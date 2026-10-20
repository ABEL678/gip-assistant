"""ProjectStandardService — бизнес-логика стандартов проекта."""

import logging
from typing import Any
from uuid import UUID

from backend.src.domain.entities.project_standard import ProjectStandard
from backend.src.domain.ports.repositories import ProjectStandardRepository
from backend.src.domain.value_objects.enums import ProjectStandardType

logger = logging.getLogger(__name__)


class ProjectStandardService:
    """Сервис работы со стандартами проекта (ProjectStandard)."""

    def __init__(self, repo: ProjectStandardRepository) -> None:
        self._repo = repo

    async def get_by_id(self, standard_id: UUID) -> ProjectStandard | None:
        """Найти стандарт по ID."""
        return await self._repo.get_by_id(standard_id)

    async def list_by_premise(self, premise_id: UUID) -> list[ProjectStandard]:
        """Стандарты вводной."""
        return await self._repo.list_by_premise(premise_id)

    async def list_by_type(self, type: ProjectStandardType) -> list[ProjectStandard]:
        """Стандарты типа."""
        return await self._repo.list_by_type(type)

    async def create(
        self,
        premise_id: UUID,
        type: ProjectStandardType,
        value: dict[str, Any] | None = None,
    ) -> ProjectStandard:
        """Создать стандарт проекта.

        Args:
            premise_id: UUID вводной.
            type: Тип стандарта.
            value: Значение (словарь).

        """
        standard = ProjectStandard(
            premise_id=premise_id,
            type=type,
            value=value or {},
        )
        return await self._repo.save(standard)

    async def update(
        self,
        standard_id: UUID,
        premise_id: UUID | None = None,
        type: ProjectStandardType | None = None,
        value: dict[str, Any] | None = None,
    ) -> ProjectStandard:
        """Обновить стандарт проекта.

        Args:
            standard_id: UUID стандарта.

        Raises:
            ValueError: если стандарт не найден.
        """
        standard = await self._repo.get_by_id(standard_id)
        if standard is None:
            raise ValueError(f"Стандарт {standard_id} не найден")

        if premise_id is not None:
            standard.premise_id = premise_id
        if type is not None:
            standard.type = type
        if value is not None:
            standard.value = value

        return await self._repo.save(standard)

    async def delete(self, standard_id: UUID) -> None:
        """Удалить стандарт проекта.

        Raises:
            ValueError: если стандарт не найден.
        """
        standard = await self._repo.get_by_id(standard_id)
        if standard is None:
            raise ValueError(f"Стандарт {standard_id} не найден")

        await self._repo.delete(standard_id)
