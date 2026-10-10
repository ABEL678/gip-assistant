"""EntityService — бизнес-логика экземпляров пользовательских сущностей.

Реализация ТЗ 4.0, раздел 5.4.
"""

import logging
from typing import Any
from uuid import UUID

from backend.src.domain.entities.entity import Entity
from backend.src.domain.ports.repositories import (
    EntityRepository,
    EntityTypeRepository,
)

logger = logging.getLogger(__name__)


class EntityService:
    """Сервис работы с экземплярами сущностей."""

    def __init__(
        self,
        repo: EntityRepository,
        entity_type_repo: EntityTypeRepository,
    ) -> None:
        self._repo = repo
        self._entity_type_repo = entity_type_repo

    async def create(
            self,
            project_id: UUID,
            entity_type_id: UUID,
            data: dict[str, Any],
            sort_order: int = 0,
    ) -> Entity:
        """Создать запись. Проверяет, что тип существует, принадлежит проекту,
        и данные валидны.
        """
        entity_type = await self._entity_type_repo.get_by_id(entity_type_id)
        if entity_type is None:
            raise ValueError(f"Тип сущности {entity_type_id} не найден")

        # Нормализуем оба ID к UUID для безопасного сравнения
        if UUID(str(entity_type.project_id)) != UUID(str(project_id)):
            raise ValueError(
                f"Тип сущности {entity_type_id} принадлежит другому проекту"
            )

        _validate_data(data, entity_type.field_schema or {})

        entity = Entity(
            project_id=project_id,
            entity_type_id=entity_type_id,
            data=data,
            sort_order=sort_order,
        )
        return await self._repo.save(entity)

    async def get_by_id(self, entity_id: UUID) -> Entity | None:
        return await self._repo.get_by_id(entity_id)

    async def list_by_type(self, entity_type_id: UUID) -> list[Entity]:
        return await self._repo.list_by_type(entity_type_id)

    async def update(
        self,
        entity_id: UUID,
        *,
        data: dict[str, Any] | None = None,
        sort_order: int | None = None,
    ) -> Entity | None:
        """Обновить запись."""
        entity = await self._repo.get_by_id(entity_id)
        if entity is None:
            return None

        if data is not None:
            entity_type = await self._entity_type_repo.get_by_id(entity.entity_type_id)
            if entity_type is not None:
                _validate_data(data, entity_type.field_schema or {})
            entity.data = data
        if sort_order is not None:
            entity.sort_order = sort_order

        return await self._repo.save(entity)

    async def delete(self, entity_id: UUID) -> bool:
        """Удалить запись. True — если удалено, False — если не найдено."""
        entity = await self._repo.get_by_id(entity_id)
        if entity is None:
            return False
        await self._repo.delete(entity_id)
        return True


def _validate_data(data: dict[str, Any], schema: dict) -> None:
    """Проверить, что обязательные поля присутствуют."""
    fields = schema.get("fields", [])
    for field in fields:
        if not isinstance(field, dict):
            continue
        key = field.get("key")
        if not key:
            continue
        if field.get("required") and key not in data:
            raise ValueError(
                f"Поле '{field.get('label', key)}' обязательно для заполнения"
            )