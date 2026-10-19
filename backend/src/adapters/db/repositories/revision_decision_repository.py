"""SQLAlchemy-реализация RevisionDecisionRepository."""

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.revision_decision import (
    RevisionDecisionModel,
)
from backend.src.domain.entities.revision_decision import RevisionDecision
from backend.src.domain.ports.repositories import RevisionDecisionRepository
from backend.src.domain.value_objects.enums import RevisionDecisionType


class SqlAlchemyRevisionDecisionRepository(RevisionDecisionRepository):
    """Репозиторий решений ГИП на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, decision_id: UUID) -> RevisionDecision | None:
        stmt = select(RevisionDecisionModel).where(RevisionDecisionModel.id == decision_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_by_change(
        self,
        change_id: UUID,
    ) -> list[RevisionDecision]:
        stmt = (
            select(RevisionDecisionModel)
            .where(RevisionDecisionModel.change_id == change_id)
            .order_by(RevisionDecisionModel.created_at)
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(
        self,
        decision: RevisionDecision,
    ) -> RevisionDecision:
        model = self._to_model(decision)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return self._to_domain(merged)

    async def delete(self, decision_id: UUID) -> None:
        stmt = delete(RevisionDecisionModel).where(RevisionDecisionModel.id == decision_id)
        await self._session.execute(stmt)
        await self._session.flush()

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(
        model: RevisionDecisionModel,
    ) -> RevisionDecision:
        return RevisionDecision(
            id=model.id,
            change_id=model.change_id,
            decision=RevisionDecisionType(model.decision),
            decided_by=model.decided_by,
            deadline=model.deadline,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: RevisionDecision) -> RevisionDecisionModel:
        return RevisionDecisionModel(
            id=domain.id,
            change_id=domain.change_id,
            decision=domain.decision.value,
            decided_by=domain.decided_by,
            deadline=domain.deadline,
        )
