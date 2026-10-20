"""SQLAlchemy-реализация ActionRepository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.action import ActionModel
from backend.src.domain.entities.action import Action
from backend.src.domain.ports.repositories import ActionRepository
from backend.src.domain.value_objects.enums import ActionState


class SqlAlchemyActionRepository(ActionRepository):
    """Репозиторий действий на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, action_id: UUID) -> Action | None:
        model = await self._session.get(ActionModel, action_id)
        if model is None:
            return None
        return self._to_domain(model)

    async def list_by_task(self, task_id: UUID) -> list[Action]:
        stmt = (
            select(ActionModel)
            .where(ActionModel.task_id == task_id)
            .order_by(ActionModel.created_at.desc())
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def list_by_project(self, project_id: UUID) -> list[Action]:
        stmt = (
            select(ActionModel)
            .where(ActionModel.project_id == project_id)
            .order_by(ActionModel.created_at.desc())
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, action: Action) -> Action:
        model = self._to_model(action)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return self._to_domain(merged)

    async def delete(self, action_id: UUID) -> None:
        await self._session.delete(ActionModel(id=action_id))

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: ActionModel) -> Action:
        return Action(
            id=model.id,
            project_id=model.project_id,
            formulation=model.formulation,
            task_id=model.task_id,
            measurable_result=model.measurable_result,
            deadline=model.deadline,
            responsible_id=model.responsible_id,
            state=ActionState(model.state),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: Action) -> ActionModel:
        return ActionModel(
            id=domain.id,
            project_id=domain.project_id,
            formulation=domain.formulation,
            task_id=domain.task_id,
            measurable_result=domain.measurable_result,
            deadline=domain.deadline,
            responsible_id=domain.responsible_id,
            state=domain.state.value,
        )
