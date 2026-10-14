"""SQLAlchemy-реализация DocumentLinkRepository."""

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.document_link import DocumentLinkModel
from backend.src.domain.entities.document_link import DocumentLink
from backend.src.domain.ports.repositories import DocumentLinkRepository
from backend.src.domain.value_objects.document import DocumentLinkType


class SqlAlchemyDocumentLinkRepository(DocumentLinkRepository):
    """Репозиторий связей ГОСТ-документов на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, id: UUID) -> DocumentLink | None:
        stmt = select(DocumentLinkModel).where(DocumentLinkModel.id == id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_by_source(self, document_id: UUID) -> list[DocumentLink]:
        stmt = select(DocumentLinkModel).where(
            DocumentLinkModel.source_document_id == document_id
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def list_by_target(self, document_id: UUID) -> list[DocumentLink]:
        stmt = select(DocumentLinkModel).where(
            DocumentLinkModel.target_document_id == document_id
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, link: DocumentLink) -> DocumentLink:
        model = self._to_model(link)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return self._to_domain(merged)

    async def delete(self, id: UUID) -> None:
        stmt = delete(DocumentLinkModel).where(DocumentLinkModel.id == id)
        await self._session.execute(stmt)
        await self._session.flush()

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: DocumentLinkModel) -> DocumentLink:
        return DocumentLink(
            id=model.id,
            source_document_id=model.source_document_id,
            target_document_id=model.target_document_id,
            link_type=DocumentLinkType(model.link_type),
            created_at=model.created_at,
        )

    @staticmethod
    def _to_model(domain: DocumentLink) -> DocumentLinkModel:
        return DocumentLinkModel(
            id=domain.id,
            source_document_id=domain.source_document_id,
            target_document_id=domain.target_document_id,
            link_type=domain.link_type.value,
        )
