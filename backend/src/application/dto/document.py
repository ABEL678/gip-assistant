"""DTO для ГОСТ-документов."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from backend.src.domain.value_objects.document import (
    DocPartType,
    DocumentKind,
    LifecycleStatus,
)


class DocumentBase(BaseModel):
    """Базовые поля для ГОСТ-документов."""
    document_name: str = Field(..., min_length=1, max_length=500)
    cipher: str = Field(..., min_length=1, max_length=500)
    document_kind: DocumentKind = DocumentKind.PD
    doc_part_type: Optional[DocPartType] = None
    document_type_id: uuid.UUID
    base_designation: Optional[str] = Field(None, max_length=200)
    section_code: Optional[str] = Field(None, max_length=50)
    mark: Optional[str] = Field(None, max_length=50)
    entity_id: Optional[uuid.UUID] = None
    task_id: Optional[uuid.UUID] = None
    lifecycle_status: LifecycleStatus = LifecycleStatus.DRAFT
    version_parent_id: Optional[uuid.UUID] = None
    replaces_id: Optional[uuid.UUID] = None
    replaced_by_id: Optional[uuid.UUID] = None
    rfi_id: Optional[uuid.UUID] = None
    trigger_action_id: Optional[uuid.UUID] = None


class DocumentCreate(DocumentBase):
    """DTO для создания ГОСТ-документа.

    project_id берётся из URL пути.
    guid генерируется доменом (uuid4) при создании.
    """
    pass


class DocumentUpdate(BaseModel):
    """DTO для обновления ГОСТ-документа (все поля опциональны)."""
    model_config = ConfigDict(populate_by_name=True)

    document_name: Optional[str] = Field(None, min_length=1, max_length=500)
    document_kind: Optional[DocumentKind] = None
    doc_part_type: Optional[DocPartType] = None
    section_code: Optional[str] = Field(None, max_length=50)
    mark: Optional[str] = Field(None, max_length=50)
    base_designation: Optional[str] = Field(None, max_length=200)
    lifecycle_status: Optional[LifecycleStatus] = None


class DocumentRead(DocumentBase):
    """DTO для чтения ГОСТ-документа."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    guid: uuid.UUID
    project_id: uuid.UUID
    current_version_id: Optional[uuid.UUID] = None
    signed_by: Optional[uuid.UUID] = None
    signed_at: Optional[datetime] = None
    signature_hash: Optional[str] = None
    signature_status: Optional[str] = None
    created_by: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime
