"""DocumentLinkService — бизнес-логика связей ГОСТ-документов.

Реализация ТЗ 4.4, раздел 16.
"""

import logging
from uuid import UUID

from backend.src.domain.entities.document_link import DocumentLink
from backend.src.domain.ports.repositories import (
    DocumentLinkRepository,
    DocumentRepository,
)
from backend.src.domain.value_objects.document import DocumentLinkType

logger = logging.getLogger(__name__)


class DocumentLinkService:
    """Сервис работы со связями ГОСТ-документов."""

    def __init__(
        self,
        repo: DocumentLinkRepository,
        document_repo: DocumentRepository,
    ) -> None:
        self._repo = repo
        self._document_repo = document_repo

    async def create(
        self,
        source_document_id: UUID,
        target_document_id: UUID,
        link_type: DocumentLinkType,
    ) -> DocumentLink:
        """Создать связь между документами.

        Raises:
            ValueError: если source == target, документы не найдены, или из разных проектов.
        """
        # Валидация 1: не связывать документ с самим собой
        if source_document_id == target_document_id:
            raise ValueError("Документ не может быть связан сам с собой")

        # Валидация 2: source существует
        source = await self._document_repo.get_by_id(source_document_id)
        if source is None:
            raise ValueError(f"Документ {source_document_id} не найден")

        # Валидация 3: target существует
        target = await self._document_repo.get_by_id(target_document_id)
        if target is None:
            raise ValueError(f"Документ {target_document_id} не найден")

        # Валидация 4: один проект
        if UUID(str(source.project_id)) != UUID(str(target.project_id)):
            raise ValueError(
                f"Нельзя связать документы из разных проектов: "
                f"{source.project_id} vs {target.project_id}"
            )

        link = DocumentLink(
            source_document_id=source_document_id,
            target_document_id=target_document_id,
            link_type=link_type,
        )
        return await self._repo.save(link)

    async def get_by_id(self, id: UUID) -> DocumentLink | None:
        return await self._repo.get_by_id(id)

    async def list_by_source(self, document_id: UUID) -> list[DocumentLink]:
        return await self._repo.list_by_source(document_id)

    async def list_by_target(self, document_id: UUID) -> list[DocumentLink]:
        return await self._repo.list_by_target(document_id)

    async def delete(self, id: UUID) -> bool:
        """Удалить связь ГОСТ-документов.

        Возвращает True, если удалено. False, если не найдено.
        """
        link = await self._repo.get_by_id(id)
        if link is None:
            return False

        await self._repo.delete(id)
        return True
