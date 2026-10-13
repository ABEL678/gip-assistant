"""Доменная сущность DocumentVersion (версия файла документа)."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class DocumentVersion:
    document_id: UUID
    version: str  # v1.0, v1.1
    file_path: str
    file_name: str
    hash_sha256: str
    format_original: str
    size_bytes: int
    id: UUID = field(default_factory=uuid4)
    change_number: int | None = None
    format_archive: str | None = None
    is_current: bool = False
    uploaded_by: UUID | None = None
    uploaded_at: datetime | None = None
