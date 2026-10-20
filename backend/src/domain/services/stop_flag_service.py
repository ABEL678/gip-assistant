"""StopFlagService — бизнес-логика стоп-сигналов."""

import logging
from uuid import UUID

from backend.src.domain.entities.stop_flag import StopFlag
from backend.src.domain.ports.repositories import StopFlagRepository

logger = logging.getLogger(__name__)


class StopFlagService:
    """Сервис работы со стоп-сигналами (StopFlag)."""

    def __init__(self, repo: StopFlagRepository) -> None:
        self._repo = repo

    async def get_by_id(self, stop_flag_id: UUID) -> StopFlag | None:
        """Найти стоп-сигнал по ID."""
        return await self._repo.get_by_id(stop_flag_id)

    async def list_by_revision(self, revision_id: UUID) -> list[StopFlag]:
        """Стоп-сигналы ревизии."""
        return await self._repo.list_by_revision(revision_id)

    async def create(
        self,
        revision_id: UUID,
        reason: str,
        resolved: bool = False,
    ) -> StopFlag:
        """Создать стоп-сигнал.

        Args:
            revision_id: UUID ревизии.
            reason: Причина стоп-сигнала.
            resolved: Разрешён ли.

        Raises:
            ValueError: если reason пустой после strip.
        """
        reason = reason.strip()
        if not reason:
            raise ValueError("Причина стоп-сигнала не может быть пустой")

        stop_flag = StopFlag(
            revision_id=revision_id,
            reason=reason,
            resolved=resolved,
        )
        return await self._repo.save(stop_flag)

    async def delete(self, stop_flag_id: UUID) -> None:
        """Удалить стоп-сигнал.

        Raises:
            ValueError: если стоп-сигнал не найден.
        """
        stop_flag = await self._repo.get_by_id(stop_flag_id)
        if stop_flag is None:
            raise ValueError(f"Стоп-сигнал {stop_flag_id} не найден")

        await self._repo.delete(stop_flag_id)
