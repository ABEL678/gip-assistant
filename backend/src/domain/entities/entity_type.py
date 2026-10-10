# backend/src/domain/entities/entity_type.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass
class EntityType:
    """
    Тип пользовательской сущности.

    Например: «Исходные данные», «Запросы», «Протоколы».
    Содержит схему полей (JSONB).
    """
    project_id: UUID
    name: str
    icon: str = "📄"
    color: str = "gray"
    description: str | None = None
    field_schema: dict[str, Any] = field(default_factory=dict)
    is_system: bool = False
    sort_order: int = 0
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None