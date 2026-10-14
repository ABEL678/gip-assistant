"""DocumentTypeService — бизнес-логика типов ГОСТ-документов.

Реализация ТЗ 4.4, раздел 16.
"""

import logging
from uuid import UUID

from backend.src.domain.entities.document_type import DocumentType
from backend.src.domain.ports.repositories import DocumentTypeRepository

logger = logging.getLogger(__name__)


class DocumentTypeService:
    """Сервис работы с типами ГОСТ-документов."""

    def __init__(self, repo: DocumentTypeRepository) -> None:
        self._repo = repo

    async def create(
        self,
        code: str,
        name: str,
        description: str | None = None,
        gost_code: str | None = None,
    ) -> DocumentType:
        """Создать тип ГОСТ-документа."""
        existing = await self._repo.get_by_code(code)
        if existing is not None:
            raise ValueError(f"Тип с кодом '{code}' уже существует")

        document_type = DocumentType(
            code=code,
            name=name,
            description=description,
            gost_code=gost_code,
        )
        return await self._repo.save(document_type)

    async def get_by_id(self, id: UUID) -> DocumentType | None:
        return await self._repo.get_by_id(id)

    async def get_by_code(self, code: str) -> DocumentType | None:
        return await self._repo.get_by_code(code)

    async def list_all(self) -> list[DocumentType]:
        return await self._repo.list_all()

    async def update(
        self,
        id: UUID,
        *,
        name: str | None = None,
        description: str | None = None,
        gost_code: str | None = None,
    ) -> DocumentType | None:
        """Обновить тип ГОСТ-документа."""
        document_type = await self._repo.get_by_id(id)
        if document_type is None:
            return None

        if name is not None:
            document_type.name = name
        if description is not None:
            document_type.description = description
        if gost_code is not None:
            document_type.gost_code = gost_code

        return await self._repo.save(document_type)

    async def delete(self, id: UUID) -> bool:
        """Удалить тип ГОСТ-документа.

        Возвращает True, если удалено. False, если не найдено.
        """
        document_type = await self._repo.get_by_id(id)
        if document_type is None:
            return False

        await self._repo.delete(id)
        return True
