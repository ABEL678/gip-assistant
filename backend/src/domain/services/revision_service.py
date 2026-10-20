"""RevisionService — бизнес-логика версий документов."""

import logging
from uuid import UUID

from backend.src.domain.entities.revision import Revision
from backend.src.domain.ports.repositories import RevisionRepository

logger = logging.getLogger(__name__)


class RevisionService:
    """Сервис работы с ревизиями (Revision)."""

    def __init__(self, repo: RevisionRepository) -> None:
        self._repo = repo

    async def get_by_id(self, revision_id: UUID) -> Revision | None:
        """Найти ревизию по ID."""
        return await self._repo.get_by_id(revision_id)

    async def list_by_document(self, document_id: UUID) -> list[Revision]:
        """Ревизии документа."""
        return await self._repo.list_by_document(document_id)

    async def create(
        self,
        document_id: UUID,
        version: int,
        date=None,
        source: str | None = None,
        notified: bool = False,
        stop_flag: bool = False,
    ) -> Revision:
        """Создать ревизию.

        Args:
            document_id: UUID документа.
            version: Номер версии (>= 1).
            date: Дата ревизии.
            source: Источник.
            notified: Уведомлены ли участники.
            stop_flag: Стоп-сигнал.

        Raises:
            ValueError: если version < 1.
        """
        if version < 1:
            raise ValueError("Версия должна быть >= 1")

        revision = Revision(
            document_id=document_id,
            version=version,
            date=date,
            source=source,
            notified=notified,
            stop_flag=stop_flag,
        )
        return await self._repo.save(revision)

    async def delete(self, revision_id: UUID) -> None:
        """Удалить ревизию.

        Raises:
            ValueError: если ревизия не найдена.
        """
        revision = await self._repo.get_by_id(revision_id)
        if revision is None:
            raise ValueError(f"Ревизия {revision_id} не найдена")

        await self._repo.delete(revision_id)
