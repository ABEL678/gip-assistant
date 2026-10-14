"""SQLAlchemy-реализация DocumentVersionRepository."""

from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.document_version import DocumentVersionModel
from backend.src.domain.entities.document_version import DocumentVersion
from backend.src.domain.ports.repositories import DocumentVersionRepository


class SqlAlchemyDocumentVersionRepository(DocumentVersionRepository):
    """Репозиторий версий ГОСТ-документов на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, id: UUID) -> DocumentVersion | None:
        stmt = select(DocumentVersionModel).where(DocumentVersionModel.id == id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_by_document(self, document_id: UUID) -> list[DocumentVersion]:
        stmt = (
            select(DocumentVersionModel)
            .where(DocumentVersionModel.document_id == document_id)
            .order_by(DocumentVersionModel.uploaded_at.desc())
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def get_current(self, document_id: UUID) -> DocumentVersion | None:
        stmt = (
            select(DocumentVersionModel)
            .where(
                DocumentVersionModel.document_id == document_id,
                DocumentVersionModel.is_current.is_(True),
            )
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def save(self, version: DocumentVersion) -> DocumentVersion:
        model = self._to_model(version)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return self._to_domain(merged)

    async def set_current(self, document_id: UUID, version_id: UUID) -> None:
        stmt_reset = (
            update(DocumentVersionModel)
            .where(DocumentVersionModel.document_id == document_id)
            .values(is_current=False)
        )
        await self._session.execute(stmt_reset)

        stmt_set = (
            update(DocumentVersionModel)
            .where(
                DocumentVersionModel.id == version_id,
                DocumentVersionModel.document_id == document_id,
            )
            .values(is_current=True)
        )
        await self._session.execute(stmt_set)
        await self._session.flush()

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: DocumentVersionModel) -> DocumentVersion:
        return DocumentVersion(
            id=model.id,
            document_id=model.document_id,
            version=model.version,
            change_number=model.change_number,
            file_path=model.file_path,
            file_name=model.file_name,
            hash_sha256=model.hash_sha256,
            format_original=model.format_original,
            format_archive=model.format_archive,
            size_bytes=model.size_bytes,
            is_current=model.is_current,
            uploaded_by=model.uploaded_by,
            uploaded_at=model.uploaded_at,
        )

    @staticmethod
    def _to_model(domain: DocumentVersion) -> DocumentVersionModel:
        return DocumentVersionModel(
            id=domain.id,
            document_id=domain.document_id,
            version=domain.version,
            change_number=domain.change_number,
            file_path=domain.file_path,
            file_name=domain.file_name,
            hash_sha256=domain.hash_sha256,
            format_original=domain.format_original,
            format_archive=domain.format_archive,
            size_bytes=domain.size_bytes,
            is_current=domain.is_current,
            uploaded_by=domain.uploaded_by,
        )
