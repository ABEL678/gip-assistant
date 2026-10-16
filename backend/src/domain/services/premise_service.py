"""PremiseService — бизнес-логика вводных."""

import logging
from uuid import UUID

from backend.src.domain.entities.premise import Premise
from backend.src.domain.ports.repositories import PremiseRepository
from backend.src.domain.value_objects.enums import PremiseCategory

logger = logging.getLogger(__name__)


class PremiseService:
    """Сервис работы с вводными (Premise)."""

    def __init__(self, repo: PremiseRepository) -> None:
        self._repo = repo

    async def get(self, premise_id: UUID) -> Premise | None:
        """Найти вводную по ID."""
        return await self._repo.get_by_id(premise_id)

    async def list_by_project(self, project_id: UUID) -> list[Premise]:
        """Список вводных проекта."""
        return await self._repo.list_by_project(project_id)

    async def create(
        self,
        project_id: UUID,
        category: PremiseCategory,
        name: str,
        **kwargs,
    ) -> Premise:
        """Создать вводную.

        Args:
            project_id: UUID проекта.
            category: Категория вводной.
            name: Название (не пустое).

        Kwargs:
            source, date, actual, mandatory, link, valid_until, data, schema.

        Raises:
            ValueError: если name пустое после strip.
        """
        name = name.strip()
        if not name:
            raise ValueError("Название вводной не может быть пустым")

        premise = Premise(
            project_id=project_id,
            category=category,
            name=name,
            **kwargs,
        )
        return await self._repo.save(premise)

    async def update(
        self,
        premise_id: UUID,
        **kwargs,
    ) -> Premise:
        """Обновить вводную.

        Args:
            premise_id: UUID вводной.

        Raises:
            ValueError: если вводная не найдена.
        """
        premise = await self._repo.get_by_id(premise_id)
        if premise is None:
            raise ValueError(f"Вводная {premise_id} не найдена")

        for key, value in kwargs.items():
            if value is not None and hasattr(premise, key):
                setattr(premise, key, value)

        return await self._repo.save(premise)

    async def delete(self, premise_id: UUID) -> None:
        """Удалить вводную.

        Raises:
            ValueError: если вводная не найдена.
        """
        premise = await self._repo.get_by_id(premise_id)
        if premise is None:
            raise ValueError(f"Вводная {premise_id} не найдена")

        await self._repo.delete(premise_id)
