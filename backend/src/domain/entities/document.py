"""Доменная сущность Document (ГОСТ Р 21.101-2026)."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from backend.src.domain.value_objects.document import (
    DocumentKind,
    DocPartType,
    LifecycleStatus,
)


@dataclass
class Document:
    # Обязательные (без default)
    project_id: UUID
    document_type_id: UUID

    # Опциональные (с default)
    guid: UUID = field(default_factory=uuid4)
    cipher: str = ""
    document_name: str = ""
    document_kind: DocumentKind = DocumentKind.PD
    doc_part_type: DocPartType | None = None
    section_code: str | None = None
    mark: str | None = None
    base_designation: str | None = None
    entity_id: UUID | None = None
    task_id: UUID | None = None
    premise_id: UUID | None = None
    current_version_id: UUID | None = None  # НЕ FK
    version_parent_id: UUID | None = None
    replaces_id: UUID | None = None
    replaced_by_id: UUID | None = None
    lifecycle_status: LifecycleStatus = LifecycleStatus.DRAFT
    signed_by: UUID | None = None
    signed_at: datetime | None = None
    signature_hash: str | None = None
    signature_status: str | None = None
    created_by: UUID | None = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None
