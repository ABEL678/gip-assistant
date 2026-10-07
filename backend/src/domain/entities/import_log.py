"""Доменная сущность ImportLog."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from backend.src.domain.value_objects.enums import ImportStatus


@dataclass
class ImportLog:
    """Лог импорта Excel."""

    project_id: UUID
    filename: str | None = None
    rows_imported: int = 0
    rows_failed: int = 0
    status: ImportStatus = ImportStatus.SUCCESS
    column_mapping: dict | None = None
    error_details: dict | None = None
    id: UUID = field(default_factory=uuid4)
    imported_at: datetime | None = None