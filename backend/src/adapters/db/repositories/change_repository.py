"""SQLAlchemy-реализация ChangeRepository."""

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.change import ChangeModel
from backend.src.domain.entities.change import Change
from backend.src.domain.ports.repositories import ChangeRepository
from backend.src.domain.value_objects.enums import ChangeStatus


class SqlAlchemyChangeRepository(ChangeRepository):
    """Репозиторий изменений на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, change_id: UUID) -> Change | None:
        stmt = select(ChangeModel).where(ChangeModel.id == change_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_by_revision(self, revision_id: UUID) -> list[Change]:
        stmt = (
            select(ChangeModel)
            .where(ChangeModel.revision_id == revision_id)
            .order_by(ChangeModel.field)
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, change: Change) -> Change:
        model = self._to_model(change)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return self._to_domain(merged)

    async def delete(self, change_id: UUID) -> None:
        stmt = delete(ChangeModel).where(ChangeModel.id == change_id)
        await self._session.execute(stmt)
        await self._session.flush()

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: ChangeModel) -> Change:
        return Change(
            id=model.id,
            revision_id=model.revision_id,
            field=model.field,
            old_value=model.old_value,
            new_value=model.new_value,
            status=ChangeStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: Change) -> ChangeModel:
        return ChangeModel(
            id=domain.id,
            revision_id=domain.revision_id,
            field=domain.field,
            old_value=domain.old_value,
            new_value=domain.new_value,
            status=domain.status.value,
        )
