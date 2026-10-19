"""SQLAlchemy-реализация StopFlagRepository."""

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.stop_flag import StopFlagModel
from backend.src.domain.entities.stop_flag import StopFlag
from backend.src.domain.ports.repositories import StopFlagRepository


class SqlAlchemyStopFlagRepository(StopFlagRepository):
    """Репозиторий стоп-сигналов на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, stop_flag_id: UUID) -> StopFlag | None:
        stmt = select(StopFlagModel).where(StopFlagModel.id == stop_flag_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_by_revision(self, revision_id: UUID) -> list[StopFlag]:
        stmt = (
            select(StopFlagModel)
            .where(StopFlagModel.revision_id == revision_id)
            .order_by(StopFlagModel.created_at)
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, stop_flag: StopFlag) -> StopFlag:
        model = self._to_model(stop_flag)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return self._to_domain(merged)

    async def delete(self, stop_flag_id: UUID) -> None:
        stmt = delete(StopFlagModel).where(StopFlagModel.id == stop_flag_id)
        await self._session.execute(stmt)
        await self._session.flush()

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: StopFlagModel) -> StopFlag:
        return StopFlag(
            id=model.id,
            revision_id=model.revision_id,
            reason=model.reason,
            resolved=model.resolved,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: StopFlag) -> StopFlagModel:
        return StopFlagModel(
            id=domain.id,
            revision_id=domain.revision_id,
            reason=domain.reason,
            resolved=domain.resolved,
        )
