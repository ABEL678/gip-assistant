"""SQLAlchemy-реализация TaskRepository."""

from datetime import date, timedelta
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.task import Task as TaskModel
from backend.src.domain.entities.task import Task
from backend.src.domain.ports.repositories import TaskRepository
from backend.src.domain.value_objects.enums import TaskStatus


class SqlAlchemyTaskRepository(TaskRepository):
    """Репозиторий задач на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, task_id: UUID) -> Task | None:
        stmt = select(TaskModel).where(TaskModel.id == task_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_by_project(
        self, project_id: UUID, limit: int = 500, offset: int = 0
    ) -> list[Task]:
        stmt = (
            select(TaskModel)
            .where(TaskModel.project_id == project_id)
            .order_by(TaskModel.sort_order, TaskModel.created_at)
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def get_overdue(self, as_of: date | None = None) -> list[Task]:
        as_of = as_of or date.today()
        stmt = select(TaskModel).where(
            TaskModel.deadline < as_of,
            TaskModel.status.notin_([TaskStatus.DONE, TaskStatus.CANCELLED]),
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def get_upcoming(self, days: int = 3) -> list[Task]:
        today = date.today()
        horizon = today + timedelta(days=days)
        stmt = select(TaskModel).where(
            TaskModel.deadline >= today,
            TaskModel.deadline <= horizon,
            TaskModel.status.notin_([TaskStatus.DONE, TaskStatus.CANCELLED]),
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, task: Task) -> Task:
        model = self._to_model(task)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return self._to_domain(merged)

    async def bulk_save(self, tasks: list[Task]) -> list[Task]:
        models = [self._to_model(t) for t in tasks]
        self._session.add_all(models)
        await self._session.flush()
        for m in models:
            await self._session.refresh(m)  # ← НОВЫЙ ЦИКЛ
        return [self._to_domain(m) for m in models]

    async def delete(self, task_id: UUID) -> None:
        stmt = delete(TaskModel).where(TaskModel.id == task_id)
        await self._session.execute(stmt)
        await self._session.flush()

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: TaskModel) -> Task:
        return Task(
            id=model.id,
            project_id=model.project_id,
            title=model.title,
            description=model.description,
            status=model.status,
            assignee_id=model.assignee_id,
            deadline=model.deadline,
            section_code=model.section_code,
            to_section_code=model.to_section_code,
            sort_order=model.sort_order,
            source=model.source,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: Task) -> TaskModel:
        return TaskModel(
            id=domain.id,
            project_id=domain.project_id,
            title=domain.title,
            description=domain.description,
            status=domain.status,
            assignee_id=domain.assignee_id,
            deadline=domain.deadline,
            section_code=domain.section_code,
            to_section_code=domain.to_section_code,
            sort_order=domain.sort_order,
            source=domain.source,
        )