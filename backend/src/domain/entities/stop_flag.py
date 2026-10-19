"""Доменная сущность StopFlag (стоп-сигнал)."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class StopFlag:
    """Стоп-сигнал для ревизии."""

    # Обязательные
    revision_id: UUID
    reason: str

    # Опциональные
    resolved: bool = False
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None
