"""SQLAlchemy-реализация DocumentTypeRepository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.document_type import DocumentTypeModel
from backend.src.domain.entities.document_type import DocumentType
from backend.src.domain.ports.repositories import DocumentTypeRepository


class SqlAlchemyDocumentTypeRepository(DocumentTypeRepository):
    """Репозиторий типов ГОСТ-документов на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, id: UUID) -> DocumentType | None:
        stmt = select(DocumentTypeModel).where(DocumentTypeModel.id == id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_by_code(self, code: str) -> DocumentType | None:
        stmt = select(DocumentTypeModel).where(DocumentTypeModel.code == code)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[DocumentType]:
        stmt = select(DocumentTypeModel).order_by(DocumentTypeModel.code)
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: DocumentTypeModel) -> DocumentType:
        return DocumentType(
            id=model.id,
            code=model.code,
            name=model.name,
            description=model.description,
            gost_code=model.gost_code,
            created_at=model.created_at,
        )

    @staticmethod
    def _to_model(domain: DocumentType) -> DocumentTypeModel:
        return DocumentTypeModel(
            id=domain.id,
            code=domain.code,
            name=domain.name,
            description=domain.description,
            gost_code=domain.gost_code,
        )
