"""SQLAlchemy-реализация PremiseRepository."""

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.premise import PremiseModel
from backend.src.domain.entities.premise import Premise
from backend.src.domain.ports.repositories import PremiseRepository
from backend.src.domain.value_objects.enums import PremiseCategory


class SqlAlchemyPremiseRepository(PremiseRepository):
    """Репозиторий вводных на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, premise_id: UUID) -> Premise | None:
        model = await self._session.get(PremiseModel, premise_id)
        return self._to_domain(model) if model else None

    async def list_by_project(self, project_id: UUID) -> list[Premise]:
        stmt = (
            select(PremiseModel)
            .where(PremiseModel.project_id == project_id)
            .order_by(PremiseModel.created_at.desc())
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def list_by_source_goal(self, goal_id: UUID) -> list[Premise]:
        stmt = select(PremiseModel).where(
            PremiseModel.source_goal_id == goal_id
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, premise: Premise) -> Premise:
        model = self._to_model(premise)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return self._to_domain(merged)

    async def delete(self, premise_id: UUID) -> None:
        stmt = delete(PremiseModel).where(PremiseModel.id == premise_id)
        await self._session.execute(stmt)
        await self._session.flush()

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: PremiseModel) -> Premise:
        return Premise(
            id=model.id,
            project_id=model.project_id,
            category=PremiseCategory(model.category),
            name=model.name,
            source=model.source,
            date=model.date,
            actual=model.actual,
            mandatory=model.mandatory,
            link=model.link,
            valid_until=model.valid_until,
            data=model.data or {},
            schema=model.schema or {},
            source_goal_id=model.source_goal_id,
            source_document_id=model.source_document_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: Premise) -> PremiseModel:
        return PremiseModel(
            id=domain.id,
            project_id=domain.project_id,
            category=domain.category.value,
            name=domain.name,
            source=domain.source,
            date=domain.date,
            actual=domain.actual,
            mandatory=domain.mandatory,
            link=domain.link,
            valid_until=domain.valid_until,
            data=domain.data or {},
            schema=domain.schema or {},
            source_goal_id=domain.source_goal_id,
            source_document_id=domain.source_document_id,
        )
