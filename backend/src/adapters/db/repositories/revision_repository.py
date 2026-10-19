"""SQLAlchemy-реализация RevisionRepository."""

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.revision import RevisionModel
from backend.src.domain.entities.revision import Revision
from backend.src.domain.ports.repositories import RevisionRepository


class SqlAlchemyRevisionRepository(RevisionRepository):
    """Репозиторий ревизий на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, revision_id: UUID) -> Revision | None:
        stmt = select(RevisionModel).where(RevisionModel.id == revision_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_by_document(self, document_id: UUID) -> list[Revision]:
        stmt = (
            select(RevisionModel)
            .where(RevisionModel.document_id == document_id)
            .order_by(RevisionModel.version.desc())
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, revision: Revision) -> Revision:
        model = self._to_model(revision)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return self._to_domain(merged)

    async def delete(self, revision_id: UUID) -> None:
        stmt = delete(RevisionModel).where(RevisionModel.id == revision_id)
        await self._session.execute(stmt)
        await self._session.flush()

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: RevisionModel) -> Revision:
        return Revision(
            id=model.id,
            document_id=model.document_id,
            version=model.version,
            date=model.date,
            source=model.source,
            notified=model.notified,
            stop_flag=model.stop_flag,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: Revision) -> RevisionModel:
        return RevisionModel(
            id=domain.id,
            document_id=domain.document_id,
            version=domain.version,
            date=domain.date,
            source=domain.source,
            notified=domain.notified,
            stop_flag=domain.stop_flag,
        )
