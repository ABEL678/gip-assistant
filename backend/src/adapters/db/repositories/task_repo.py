"""SQLAlchemy-реализация TaskRepository."""

from datetime import date, timedelta
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.document import DocumentModel
from backend.src.adapters.db.models.premise import PremiseModel
from backend.src.adapters.db.models.task import Task as TaskModel
from backend.src.domain.entities.task import Task
from backend.src.domain.ports.repositories import TaskRepository
from backend.src.domain.value_objects.enums import RfiState, TaskStatus


class SqlAlchemyTaskRepository(TaskRepository):
    """Репозиторий задач на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, task_id: UUID) -> Task | None:
        stmt = select(TaskModel).where(TaskModel.id == task_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        premise_ids = (
            await self._fetch_premise_ids(model.id)
            if model.is_rfi
            else []
        )
        return self._to_domain(model, premise_ids=premise_ids)

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
        models = result.scalars().all()
        tasks = []
        for m in models:
            premise_ids = (
                await self._fetch_premise_ids(m.id)
                if m.is_rfi
                else []
            )
            tasks.append(self._to_domain(m, premise_ids=premise_ids))
        return tasks

    async def get_by_pair(
        self,
        project_id: UUID,
        from_section: str,
        to_section: str,
    ) -> list[Task]:
        """Задачи конкретной пары (from_section → to_section).

        Сортировка: сначала просроченные (по возрастанию дедлайна),
        потом без дедлайна, потом остальные.
        """
        stmt = (
            select(TaskModel)
            .where(
                TaskModel.project_id == project_id,
                TaskModel.section_code == from_section,
                TaskModel.to_section_code == to_section,
            )
            .order_by(
                TaskModel.deadline.is_(None),  # False (есть дедлайн) — раньше
                TaskModel.deadline.asc(),
                TaskModel.created_at.asc(),
            )
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        tasks = []
        for m in models:
            premise_ids = (
                await self._fetch_premise_ids(m.id)
                if m.is_rfi
                else []
            )
            tasks.append(self._to_domain(m, premise_ids=premise_ids))
        return tasks

    async def get_overdue(self, as_of: date | None = None) -> list[Task]:
        as_of = as_of or date.today()
        stmt = select(TaskModel).where(
            TaskModel.deadline < as_of,
            TaskModel.status.notin_([TaskStatus.DONE, TaskStatus.CANCELLED]),
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        tasks = []
        for m in models:
            premise_ids = (
                await self._fetch_premise_ids(m.id)
                if m.is_rfi
                else []
            )
            tasks.append(self._to_domain(m, premise_ids=premise_ids))
        return tasks

    async def get_upcoming(self, days: int = 3) -> list[Task]:
        today = date.today()
        horizon = today + timedelta(days=days)
        stmt = select(TaskModel).where(
            TaskModel.deadline >= today,
            TaskModel.deadline <= horizon,
            TaskModel.status.notin_([TaskStatus.DONE, TaskStatus.CANCELLED]),
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        tasks = []
        for m in models:
            premise_ids = (
                await self._fetch_premise_ids(m.id)
                if m.is_rfi
                else []
            )
            tasks.append(self._to_domain(m, premise_ids=premise_ids))
        return tasks

    async def save(self, task: Task) -> Task:
        model = self._to_model(task)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        premise_ids = (
            await self._fetch_premise_ids(merged.id)
            if merged.is_rfi
            else []
        )
        return self._to_domain(merged, premise_ids=premise_ids)

    async def bulk_save(self, tasks: list[Task]) -> list[Task]:
        models = [self._to_model(t) for t in tasks]
        self._session.add_all(models)
        await self._session.flush()
        for m in models:
            await self._session.refresh(m)  # ← НОВЫЙ ЦИКЛ
        result = []
        for m in models:
            premise_ids = (
                await self._fetch_premise_ids(m.id)
                if m.is_rfi
                else []
            )
            result.append(self._to_domain(m, premise_ids=premise_ids))
        return result

    async def delete(self, task_id: UUID) -> None:
        stmt = delete(TaskModel).where(TaskModel.id == task_id)
        await self._session.execute(stmt)
        await self._session.flush()

    # ---------- Mapping ----------

    async def _fetch_premise_ids(self, task_id: UUID) -> list[UUID]:
        """Premise ID через цепочку: Task → Document → Premise.

        SELECT premise.id FROM premises
        JOIN documents ON premises.source_document_id = documents.id
        WHERE documents.rfi_id = :task_id
        """
        stmt = (
            select(PremiseModel.id)
            .join(DocumentModel, PremiseModel.source_document_id == DocumentModel.id)
            .where(DocumentModel.rfi_id == task_id)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    def _to_domain(
        self,
        model: TaskModel,
        premise_ids: list[UUID] | None = None,
    ) -> Task:
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
            is_complex=model.is_complex,
            decision_id=model.decision_id,
            is_rfi=model.is_rfi,
            rfi_cause_decision_id=model.rfi_cause_decision_id,
            rfi_cause_goal_id=model.rfi_cause_goal_id,
            rfi_due_date=model.rfi_due_date,
            rfi_state=RfiState(model.rfi_state) if model.rfi_state is not None else None,
            premise_ids=premise_ids if premise_ids is not None else [],
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
            is_complex=domain.is_complex,
            decision_id=domain.decision_id,
            is_rfi=domain.is_rfi,
            rfi_cause_decision_id=domain.rfi_cause_decision_id,
            rfi_cause_goal_id=domain.rfi_cause_goal_id,
            rfi_due_date=domain.rfi_due_date,
            rfi_state=domain.rfi_state.value if domain.rfi_state is not None else None,
        )
