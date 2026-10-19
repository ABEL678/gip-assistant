"""Доменная сущность Change (изменение между ревизиями)."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from backend.src.domain.value_objects.enums import ChangeStatus


@dataclass
class Change:
    """Что изменилось между ревизиями."""

    # Обязательные
    revision_id: UUID
    field: str
    status: ChangeStatus

    # Опциональные
    old_value: str | None = None
    new_value: str | None = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None
