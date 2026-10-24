"""SQLAlchemy-реализация RfiRepository."""

from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.task import Task as TaskModel
from backend.src.adapters.db.repositories.task_repo import SqlAlchemyTaskRepository
from backend.src.domain.entities.task import Task
from backend.src.domain.ports.repositories import RfiRepository
from backend.src.domain.value_objects.enums import RfiState


class SqlAlchemyRfiRepository(RfiRepository):
    """Репозиторий RFI (Task с is_rfi=true) на SQLAlchemy.

    Композирует SqlAlchemyTaskRepository — не дублирует _to_domain.
    premise_ids — через _fetch_premise_ids (тот же, что в TaskRepository).
    """

    def __init__(
        self,
        session: AsyncSession,
        task_repo: SqlAlchemyTaskRepository,
    ) -> None:
        self._session = session
        self._task_repo = task_repo

    async def list_rfis_by_project(self, project_id: UUID) -> list[Task]:
        """Все RFI проекта (is_rfi=true)."""
        stmt = (
            select(TaskModel)
            .where(TaskModel.project_id == project_id, TaskModel.is_rfi == True)  # noqa: E712
            .order_by(TaskModel.created_at.desc())
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        tasks = []
        for m in models:
            premise_ids = await self._task_repo._fetch_premise_ids(m.id)
            tasks.append(self._task_repo._to_domain(m, premise_ids=premise_ids))
        return tasks

    async def get_rfi_by_id(self, id: UUID) -> Task | None:
        """Найти RFI по ID."""
        stmt = select(TaskModel).where(
            TaskModel.id == id,
            TaskModel.is_rfi == True,  # noqa: E712
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        premise_ids = await self._task_repo._fetch_premise_ids(model.id)
        return self._task_repo._to_domain(model, premise_ids=premise_ids)

    async def list_by_cause_decision(self, decision_id: UUID) -> list[Task]:
        """RFI, созданные по решению."""
        stmt = (
            select(TaskModel)
            .where(
                TaskModel.rfi_cause_decision_id == decision_id,
                TaskModel.is_rfi == True,  # noqa: E712
            )
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        tasks = []
        for m in models:
            premise_ids = await self._task_repo._fetch_premise_ids(m.id)
            tasks.append(self._task_repo._to_domain(m, premise_ids=premise_ids))
        return tasks

    async def list_by_cause_goal(self, goal_id: UUID) -> list[Task]:
        """RFI, созданные по цели."""
        stmt = (
            select(TaskModel)
            .where(
                TaskModel.rfi_cause_goal_id == goal_id,
                TaskModel.is_rfi == True,  # noqa: E712
            )
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        tasks = []
        for m in models:
            premise_ids = await self._task_repo._fetch_premise_ids(m.id)
            tasks.append(self._task_repo._to_domain(m, premise_ids=premise_ids))
        return tasks

    async def list_overdue(
        self, today: date, project_id: UUID
    ) -> list[Task]:
        """Просроченные RFI проекта (rfi_due_date < today AND rfi_state NOT IN (closed, registered))."""
        stmt = (
            select(TaskModel)
            .where(
                TaskModel.project_id == project_id,
                TaskModel.is_rfi == True,  # noqa: E712
                TaskModel.rfi_due_date < today,
                TaskModel.rfi_state.notin_([RfiState.CLOSED, RfiState.REGISTERED]),
            )
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        tasks = []
        for m in models:
            premise_ids = await self._task_repo._fetch_premise_ids(m.id)
            tasks.append(self._task_repo._to_domain(m, premise_ids=premise_ids))
        return tasks
