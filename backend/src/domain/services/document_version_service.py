"""DocumentVersionService — бизнес-логика версий ГОСТ-документов.

Реализация ТЗ 4.4, раздел 16.
"""

import logging
from uuid import UUID

from backend.src.domain.entities.document_version import DocumentVersion
from backend.src.domain.ports.repositories import (
    DocumentRepository,
    DocumentVersionRepository,
)

logger = logging.getLogger(__name__)


class DocumentVersionService:
    """Сервис работы с версиями ГОСТ-документов."""

    def __init__(
        self,
        version_repo: DocumentVersionRepository,
        document_repo: DocumentRepository,
    ) -> None:
        self._version_repo = version_repo
        self._document_repo = document_repo

    async def create(
        self,
        document_id: UUID,
        version: str,
        file_path: str,
        file_name: str,
        hash_sha256: str,
        format_original: str,
        size_bytes: int,
        change_number: int | None = None,
        format_archive: str | None = None,
        uploaded_by: UUID | None = None,
    ) -> DocumentVersion:
        """Создать версию ГОСТ-документа."""
        document = await self._document_repo.get_by_id(document_id)
        if document is None:
            raise ValueError(f"Документ {document_id} не найден")

        document_version = DocumentVersion(
            document_id=document_id,
            version=version,
            file_path=file_path,
            file_name=file_name,
            hash_sha256=hash_sha256,
            format_original=format_original,
            size_bytes=size_bytes,
            change_number=change_number,
            format_archive=format_archive,
            uploaded_by=uploaded_by,
        )
        return await self._version_repo.save(document_version)

    async def get_by_id(self, id: UUID) -> DocumentVersion | None:
        return await self._version_repo.get_by_id(id)

    async def list_by_document(self, document_id: UUID) -> list[DocumentVersion]:
        return await self._version_repo.list_by_document(document_id)

    async def get_current(self, document_id: UUID) -> DocumentVersion | None:
        return await self._version_repo.get_current(document_id)

    async def set_current(self, document_id: UUID, version_id: UUID) -> None:
        """Сделать version_id текущей для document_id.

        Raises:
            ValueError: если документ или версия не найдены, или версия не принадлежит документу.
        """
        # Валидация 1: документ существует
        document = await self._document_repo.get_by_id(document_id)
        if document is None:
            raise ValueError(f"Документ {document_id} не найден")

        # Валидация 2: версия существует
        version = await self._version_repo.get_by_id(version_id)
        if version is None:
            raise ValueError(f"Версия {version_id} не найдена")

        # Валидация 3: версия принадлежит документу
        if version.document_id != document_id:
            raise ValueError(
                f"Версия {version_id} не принадлежит документу {document_id}"
            )

        # Атомарно: сбросить is_current у прежней, установить у новой
        await self._version_repo.set_current(document_id, version_id)

        # Денормализация: обновить document.current_version_id
        document.current_version_id = version_id
        await self._document_repo.save(document)

    async def delete(self, id: UUID) -> bool:
        """Удалить версию ГОСТ-документа.

        Возвращает True, если удалено. False, если не найдено.
        Если удаляется текущая версия — document.current_version_id сбрасывается в None.
        """
        version = await self._version_repo.get_by_id(id)
        if version is None:
            return False

        # Если удаляем текущую версию — сбросить current_version_id у документа
        # ДО удаления, чтобы не осталось висячей ссылки.
        if version.is_current:
            document = await self._document_repo.get_by_id(version.document_id)
            if document is not None:
                document.current_version_id = None
                await self._document_repo.save(document)

        await self._version_repo.delete(id)
        return True
