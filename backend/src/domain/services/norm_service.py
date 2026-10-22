"""NormService — бизнес-логика нормативных документов."""

import logging
from uuid import UUID

from backend.src.domain.entities.norm import Norm
from backend.src.domain.ports.repositories import NormRepository
from backend.src.domain.value_objects.enums import NormType

logger = logging.getLogger(__name__)


class NormService:
    """Сервис работы с нормативными документами (Norm)."""

    def __init__(self, repo: NormRepository) -> None:
        self._repo = repo

    async def get(self, norm_id: UUID) -> Norm | None:
        """Найти норму по ID."""
        return await self._repo.get_by_id(norm_id)

    async def list_by_project(self, project_id: UUID) -> list[Norm]:
        """Список норм проекта."""
        return await self._repo.list_by_project(project_id)

    async def create(
        self,
        project_id: UUID,
        code: str,
        title: str,
        norm_type: NormType,
        **kwargs,
    ) -> Norm:
        """Создать норму.

        Args:
            project_id: UUID проекта.
            code: Обозначение (непустое, уникально в проекте).
            title: Название (непустое).
            norm_type: Тип нормативного документа (NormType).

        Raises:
            ValueError: если code/title пустые или code уже занят в проекте.
        """
        code = code.strip()
        if not code:
            raise ValueError("Обозначение нормы не может быть пустым")

        title = title.strip()
        if not title:
            raise ValueError("Название нормы не может быть пустым")

        existing = await self._repo.get_by_code(project_id, code)
        if existing is not None:
            raise ValueError(
                f"Норма с обозначением {code} уже существует в проекте"
            )

        norm = Norm(
            project_id=project_id,
            code=code,
            title=title,
            norm_type=norm_type,
            **kwargs,
        )
        return await self._repo.save(norm)

    async def update(
        self,
        norm_id: UUID,
        **kwargs,
    ) -> Norm:
        """Обновить норму.

        Args:
            norm_id: UUID нормы.

        Raises:
            ValueError: если норма не найдена, code пустой
                или уже занят другой нормой проекта.
        """
        norm = await self._repo.get_by_id(norm_id)
        if norm is None:
            raise ValueError(f"Норма {norm_id} не найдена")

        if "code" in kwargs and kwargs["code"] is not None:
            code = kwargs["code"].strip()
            if not code:
                raise ValueError("Обозначение нормы не может быть пустым")
            existing = await self._repo.get_by_code(norm.project_id, code)
            if existing is not None and existing.id != norm_id:
                raise ValueError(
                    f"Норма с обозначением {code} уже существует в проекте"
                )
            kwargs["code"] = code

        for key, value in kwargs.items():
            if value is not None and hasattr(norm, key):
                setattr(norm, key, value)

        return await self._repo.save(norm)

    async def delete(self, norm_id: UUID) -> None:
        """Удалить норму.

        Raises:
            ValueError: если норма не найдена.
        """
        norm = await self._repo.get_by_id(norm_id)
        if norm is None:
            raise ValueError(f"Норма {norm_id} не найдена")

        await self._repo.delete(norm_id)
