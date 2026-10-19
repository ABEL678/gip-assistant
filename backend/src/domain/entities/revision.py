"""Доменная сущность Revision (версия документа)."""

from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID, uuid4


@dataclass
class Revision:
    """Версия документа, привязанная к документу (Document)."""

    # Обязательные
    document_id: UUID
    version: int

    # Опциональные
    date: date | None = None
    source: str | None = None
    notified: bool = False
    stop_flag: bool = False
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None
