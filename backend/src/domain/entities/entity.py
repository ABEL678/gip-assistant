# backend/src/domain/entities/entity.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass
class Entity:
    """
    Экземпляр пользовательской сущности.

    Например: «ТУ на водоснабжение» (запись типа «Исходные данные»).
    Данные хранятся в JSON.
    """
    project_id: UUID
    entity_type_id: UUID
    data: dict[str, Any] = field(default_factory=dict)
    sort_order: int = 0
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None