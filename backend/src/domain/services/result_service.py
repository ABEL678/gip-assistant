"""ResultService — бизнес-логика результатов проекта."""

import logging
from uuid import UUID

from backend.src.domain.entities.result import Result
from backend.src.domain.ports.repositories import ResultRepository

logger = logging.getLogger(__name__)


class ResultService:
    """Сервис работы с результатами (Result)."""

    def __init__(self, repo: ResultRepository) -> None:
        self._repo = repo

    async def get_by_id(self, result_id: UUID) -> Result | None:
        """Найти результат по ID."""
        return await self._repo.get_by_id(result_id)

    async def list_by_project(self, project_id: UUID) -> list[Result]:
        """Список результатов проекта."""
        return await self._repo.list_by_project(project_id)

    async def create(
        self,
        project_id: UUID,
        formulation: str,
        source: str | None = None,
    ) -> Result:
        """Создать результат.

        Args:
            project_id: UUID проекта.
            formulation: Формулировка результата (не пустая).
            source: Источник.

        Raises:
            ValueError: если formulation пустое после strip.
        """
        formulation = formulation.strip()
        if not formulation:
            raise ValueError("Формулировка результата не может быть пустой")

        result = Result(
            project_id=project_id,
            formulation=formulation,
            source=source,
        )
        return await self._repo.save(result)

    async def update(
        self,
        result_id: UUID,
        formulation: str | None = None,
        source: str | None = None,
    ) -> Result:
        """Обновить результат.

        Args:
            result_id: UUID результата.

        Raises:
            ValueError: если результат не найден.
        """
        result = await self._repo.get_by_id(result_id)
        if result is None:
            raise ValueError(f"Результат {result_id} не найден")

        if formulation is not None:
            result.formulation = formulation.strip()
            if not result.formulation:
                raise ValueError("Формулировка результата не может быть пустой")

        if source is not None:
            result.source = source

        return await self._repo.save(result)

    async def delete(self, result_id: UUID) -> None:
        """Удалить результат.

        Raises:
            ValueError: если результат не найден.
        """
        result = await self._repo.get_by_id(result_id)
        if result is None:
            raise ValueError(f"Результат {result_id} не найден")

        await self._repo.delete(result_id)
