"""Доменная сущность DocumentType (справочник типов документов)."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class DocumentType:
    code: str
    name: str
    id: UUID = field(default_factory=uuid4)
    description: str | None = None
    gost_code: str | None = None
    created_at: datetime | None = None
