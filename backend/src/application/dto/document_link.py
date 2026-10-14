"""DTO для связей ГОСТ-документов."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from backend.src.domain.value_objects.document import DocumentLinkType


class DocumentLinkBase(BaseModel):
    """Базовые поля для связей ГОСТ-документов."""
    source_document_id: uuid.UUID
    target_document_id: uuid.UUID
    link_type: DocumentLinkType


class DocumentLinkCreate(DocumentLinkBase):
    """DTO для создания связи ГОСТ-документов."""
    pass


class DocumentLinkRead(DocumentLinkBase):
    """DTO для чтения связи ГОСТ-документов."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    created_at: datetime
