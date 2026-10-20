"""ChangeService — бизнес-логика изменений между ревизиями."""

import logging
from uuid import UUID

from backend.src.domain.entities.change import Change
from backend.src.domain.ports.repositories import ChangeRepository
from backend.src.domain.value_objects.enums import ChangeStatus

logger = logging.getLogger(__name__)


class ChangeService:
    """Сервис работы с изменениями (Change)."""

    def __init__(self, repo: ChangeRepository) -> None:
        self._repo = repo

    async def get_by_id(self, change_id: UUID) -> Change | None:
        """Найти изменение по ID."""
        return await self._repo.get_by_id(change_id)

    async def list_by_revision(self, revision_id: UUID) -> list[Change]:
        """Изменения ревизии."""
        return await self._repo.list_by_revision(revision_id)

    async def create(
        self,
        revision_id: UUID,
        field: str,
        status: ChangeStatus,
        old_value: str | None = None,
        new_value: str | None = None,
    ) -> Change:
        """Создать изменение.

        Args:
            revision_id: UUID ревизии.
            field: Имя изменённого поля.
            status: Статус изменения.
            old_value: Старое значение.
            new_value: Новое значение.

        Raises:
            ValueError: если field пустой после strip.
        """
        field = field.strip()
        if not field:
            raise ValueError("Имя поля не может быть пустым")

        change = Change(
            revision_id=revision_id,
            field=field,
            status=status,
            old_value=old_value,
            new_value=new_value,
        )
        return await self._repo.save(change)

    async def delete(self, change_id: UUID) -> None:
        """Удалить изменение.

        Raises:
            ValueError: если изменение не найдено.
        """
        change = await self._repo.get_by_id(change_id)
        if change is None:
            raise ValueError(f"Изменение {change_id} не найдено")

        await self._repo.delete(change_id)
