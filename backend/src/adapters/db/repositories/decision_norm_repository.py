"""SQLAlchemy-реализация DecisionNormRepository."""

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.decision_norm import DecisionNormModel
from backend.src.domain.ports.repositories import DecisionNormRepository


class SqlAlchemyDecisionNormRepository(DecisionNormRepository):
    """Репозиторий связи Decision ↔ Norm (M:N) на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_norms_by_decision(self, decision_id: UUID) -> list[UUID]:
        stmt = select(DecisionNormModel.norm_id).where(
            DecisionNormModel.decision_id == decision_id
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def list_decisions_by_norm(self, norm_id: UUID) -> list[UUID]:
        stmt = select(DecisionNormModel.decision_id).where(
            DecisionNormModel.norm_id == norm_id
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def link(self, decision_id: UUID, norm_id: UUID) -> None:
        """Связать решение с нормой. Идемпотентно — ON CONFLICT DO NOTHING."""
        stmt = (
            DecisionNormModel.__table__.insert()
            .values(decision_id=decision_id, norm_id=norm_id)
            .execution_options(synchronize_session="fetch")
        )
        try:
            await self._session.execute(stmt)
            await self._session.flush()
        except IntegrityError:
            # Повторная связь — игнорируем (идемпотентность)
            await self._session.rollback()

    async def unlink(self, decision_id: UUID, norm_id: UUID) -> None:
        """Разорвать связь решения с нормой."""
        stmt = delete(DecisionNormModel).where(
            DecisionNormModel.decision_id == decision_id,
            DecisionNormModel.norm_id == norm_id,
        )
        await self._session.execute(stmt)
        await self._session.flush()
