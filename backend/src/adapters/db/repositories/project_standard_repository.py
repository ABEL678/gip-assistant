"""SQLAlchemy-реализация ProjectStandardRepository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.project_standard import ProjectStandardModel
from backend.src.adapters.db.models.standard_goal import StandardGoalModel
from backend.src.domain.entities.project_standard import ProjectStandard
from backend.src.domain.ports.repositories import ProjectStandardRepository
from backend.src.domain.value_objects.enums import ProjectStandardType


class SqlAlchemyProjectStandardRepository(ProjectStandardRepository):
    """Репозиторий стандартов проекта на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, standard_id: UUID) -> ProjectStandard | None:
        model = await self._session.get(ProjectStandardModel, standard_id)
        if model is None:
            return None
        return self._to_domain(model)

    async def list_by_premise(self, premise_id: UUID) -> list[ProjectStandard]:
        stmt = select(ProjectStandardModel).where(
            ProjectStandardModel.premise_id == premise_id
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def list_by_type(self, type: ProjectStandardType) -> list[ProjectStandard]:
        stmt = select(ProjectStandardModel).where(
            ProjectStandardModel.type == type.value
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def list_by_goal(self, goal_id: UUID) -> list[ProjectStandard]:
        stmt = (
            select(ProjectStandardModel)
            .join(
                StandardGoalModel,
                ProjectStandardModel.id == StandardGoalModel.standard_id,
            )
            .where(StandardGoalModel.goal_id == goal_id)
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, standard: ProjectStandard) -> ProjectStandard:
        model = self._to_model(standard)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return self._to_domain(merged)

    async def delete(self, standard_id: UUID) -> None:
        await self._session.delete(ProjectStandardModel(id=standard_id))

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: ProjectStandardModel) -> ProjectStandard:
        return ProjectStandard(
            id=model.id,
            premise_id=model.premise_id,
            type=ProjectStandardType(model.type),
            value=model.value,
            approved_by=model.approved_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: ProjectStandard) -> ProjectStandardModel:
        return ProjectStandardModel(
            id=domain.id,
            premise_id=domain.premise_id,
            type=domain.type.value,
            value=domain.value,
            approved_by=domain.approved_by,
        )
