"""SQLAlchemy-реализация DecisionLinkRepository."""

from uuid import UUID

from sqlalchemy import delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.decision_link import DecisionLinkModel
from backend.src.domain.entities.decision_link import DecisionLink
from backend.src.domain.ports.repositories import DecisionLinkRepository
from backend.src.domain.value_objects.enums import DecisionLinkType


class SqlAlchemyDecisionLinkRepository(DecisionLinkRepository):
    """Репозиторий связей решений на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, link_id: UUID) -> DecisionLink | None:
        model = await self._session.get(DecisionLinkModel, link_id)
        if model is None:
            return None
        return self._to_domain(model)

    async def list_by_decision(self, decision_id: UUID) -> list[DecisionLink]:
        stmt = (
            select(DecisionLinkModel)
            .where(
                or_(
                    DecisionLinkModel.from_decision_id == decision_id,
                    DecisionLinkModel.to_decision_id == decision_id,
                )
            )
            .order_by(DecisionLinkModel.created_at.desc())
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def list_by_project(self, project_id: UUID) -> list[DecisionLink]:
        stmt = (
            select(DecisionLinkModel)
            .where(DecisionLinkModel.project_id == project_id)
            .order_by(DecisionLinkModel.created_at.desc())
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, link: DecisionLink) -> DecisionLink:
        model = self._to_model(link)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return await self.get_by_id(merged.id)

    async def delete(self, link_id: UUID) -> None:
        stmt = delete(DecisionLinkModel).where(DecisionLinkModel.id == link_id)
        await self._session.execute(stmt)
        await self._session.flush()

    # ---------- Mapping ----------

    def _to_domain(self, model: DecisionLinkModel) -> DecisionLink:
        return DecisionLink(
            id=model.id,
            project_id=model.project_id,
            from_decision_id=model.from_decision_id,
            to_decision_id=model.to_decision_id,
            link_type=DecisionLinkType(model.link_type),
            created_at=model.created_at,
        )

    @staticmethod
    def _to_model(domain: DecisionLink) -> DecisionLinkModel:
        return DecisionLinkModel(
            id=domain.id,
            project_id=domain.project_id,
            from_decision_id=domain.from_decision_id,
            to_decision_id=domain.to_decision_id,
            link_type=domain.link_type.value,
        )
