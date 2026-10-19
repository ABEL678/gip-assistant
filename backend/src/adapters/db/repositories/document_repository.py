"""SQLAlchemy-реализация DocumentRepository."""

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.document import DocumentModel
from backend.src.domain.entities.document import Document
from backend.src.domain.ports.repositories import DocumentRepository
from backend.src.domain.value_objects.document import (
    DocPartType,
    DocumentKind,
    LifecycleStatus,
)


class SqlAlchemyDocumentRepository(DocumentRepository):
    """Репозиторий ГОСТ-документов на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, id: UUID) -> Document | None:
        stmt = select(DocumentModel).where(DocumentModel.id == id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_by_guid(self, guid: UUID) -> Document | None:
        stmt = select(DocumentModel).where(DocumentModel.guid == guid)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_by_project(
        self,
        project_id: UUID,
        *,
        lifecycle_status: LifecycleStatus | None = None,
    ) -> list[Document]:
        stmt = select(DocumentModel).where(DocumentModel.project_id == project_id)
        if lifecycle_status is not None:
            stmt = stmt.where(DocumentModel.lifecycle_status == lifecycle_status.value)
        stmt = stmt.order_by(DocumentModel.created_at.desc())
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, document: Document) -> Document:
        model = self._to_model(document)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return self._to_domain(merged)

    async def delete(self, id: UUID) -> None:
        stmt = delete(DocumentModel).where(DocumentModel.id == id)
        await self._session.execute(stmt)
        await self._session.flush()

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: DocumentModel) -> Document:
        return Document(
            id=model.id,
            guid=model.guid,
            project_id=model.project_id,
            entity_id=model.entity_id,
            task_id=model.task_id,
            premise_id=model.premise_id,
            cipher=model.cipher,
            document_name=model.document_name,
            document_kind=DocumentKind(model.document_kind),
            doc_part_type=DocPartType(model.doc_part_type) if model.doc_part_type else None,
            section_code=model.section_code,
            mark=model.mark,
            base_designation=model.base_designation,
            document_type_id=model.document_type_id,
            current_version_id=model.current_version_id,
            version_parent_id=model.version_parent_id,
            replaces_id=model.replaces_id,
            replaced_by_id=model.replaced_by_id,
            lifecycle_status=LifecycleStatus(model.lifecycle_status),
            signed_by=model.signed_by,
            signed_at=model.signed_at,
            signature_hash=model.signature_hash,
            signature_status=model.signature_status,
            created_by=model.created_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: Document) -> DocumentModel:
        return DocumentModel(
            id=domain.id,
            guid=domain.guid,
            project_id=domain.project_id,
            entity_id=domain.entity_id,
            task_id=domain.task_id,
            premise_id=domain.premise_id,
            cipher=domain.cipher,
            document_name=domain.document_name,
            document_kind=domain.document_kind.value,
            doc_part_type=domain.doc_part_type.value if domain.doc_part_type else None,
            section_code=domain.section_code,
            mark=domain.mark,
            base_designation=domain.base_designation,
            document_type_id=domain.document_type_id,
            current_version_id=domain.current_version_id,
            version_parent_id=domain.version_parent_id,
            replaces_id=domain.replaces_id,
            replaced_by_id=domain.replaced_by_id,
            lifecycle_status=domain.lifecycle_status.value,
            signed_by=domain.signed_by,
            signed_at=domain.signed_at,
            signature_hash=domain.signature_hash,
            signature_status=domain.signature_status,
            created_by=domain.created_by,
        )
