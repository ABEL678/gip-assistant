"""Доменная сущность DocumentLink (связь между документами)."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from backend.src.domain.value_objects.document import DocumentLinkType


@dataclass
class DocumentLink:
    source_document_id: UUID
    target_document_id: UUID
    link_type: DocumentLinkType
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
