"""EntityTypeService — бизнес-логика типов пользовательских сущностей.

Реализация ТЗ 4.0, раздел 5.4.
"""

import logging
from uuid import UUID

from backend.src.domain.entities.entity_type import EntityType
from backend.src.domain.ports.repositories import EntityTypeRepository

logger = logging.getLogger(__name__)


class EntityTypeService:
    """Сервис работы с типами сущностей."""

    def __init__(self, repo: EntityTypeRepository) -> None:
        self._repo = repo

    async def create(
        self,
        project_id: UUID,
        name: str,
        icon: str = "📄",
        color: str = "gray",
        description: str | None = None,
        field_schema: dict | None = None,
        sort_order: int = 0,
    ) -> EntityType:
        """Создать тип сущности."""
        schema = field_schema or {"fields": []}
        _validate_schema(schema)

        entity_type = EntityType(
            project_id=project_id,
            name=name,
            icon=icon,
            color=color,
            description=description,
            field_schema=schema,
            sort_order=sort_order,
        )
        return await self._repo.save(entity_type)

    async def get_by_id(self, entity_type_id: UUID) -> EntityType | None:
        """Получить тип по ID."""
        return await self._repo.get_by_id(entity_type_id)

    async def list_by_project(self, project_id: UUID) -> list[EntityType]:
        """Список типов проекта."""
        return await self._repo.list_by_project(project_id)

    async def update(
        self,
        entity_type_id: UUID,
        *,
        name: str | None = None,
        icon: str | None = None,
        color: str | None = None,
        description: str | None = None,
        field_schema: dict | None = None,
        sort_order: int | None = None,
    ) -> EntityType | None:
        """Обновить тип сущности."""
        entity_type = await self._repo.get_by_id(entity_type_id)
        if entity_type is None:
            return None

        if field_schema is not None:
            _validate_schema(field_schema)
            entity_type.field_schema = field_schema
        if name is not None:
            entity_type.name = name
        if icon is not None:
            entity_type.icon = icon
        if color is not None:
            entity_type.color = color
        if description is not None:
            entity_type.description = description
        if sort_order is not None:
            entity_type.sort_order = sort_order

        return await self._repo.save(entity_type)

    async def delete(self, entity_type_id: UUID) -> bool:
        """Удалить тип сущности.

        Возвращает True, если удалено. False, если не найдено.
        Кидает ValueError, если тип системный.
        """
        entity_type = await self._repo.get_by_id(entity_type_id)
        if entity_type is None:
            return False
        if entity_type.is_system:
            raise ValueError("Нельзя удалить системный тип сущности")
        await self._repo.delete(entity_type_id)
        return True


def _validate_schema(schema: dict) -> None:
    """Проверить, что ключи полей уникальны."""
    fields = schema.get("fields", [])
    keys = [f.get("key") for f in fields if isinstance(f, dict)]
    if len(keys) != len(set(keys)):
        raise ValueError("Ключи полей (key) должны быть уникальны")