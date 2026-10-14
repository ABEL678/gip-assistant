"""DTO для версий ГОСТ-документов."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DocumentVersionBase(BaseModel):
    """Базовые поля для версий ГОСТ-документов."""
    version: str = Field(..., min_length=1, max_length=20)
    file_path: str = Field(..., min_length=1, max_length=1000)
    file_name: str = Field(..., min_length=1, max_length=500)
    hash_sha256: str = Field(..., min_length=64, max_length=64)
    format_original: str = Field(..., min_length=1, max_length=20)
    format_archive: Optional[str] = Field(None, max_length=20)
    size_bytes: int = Field(..., ge=0)
    change_number: Optional[int] = Field(None, ge=0)


class DocumentVersionCreate(DocumentVersionBase):
    """DTO для создания версии ГОСТ-документа.

    document_id берётся из URL пути.
    is_current устанавливается отдельным вызовом set_current.
    """
    pass


class DocumentVersionRead(DocumentVersionBase):
    """DTO для чтения версии ГОСТ-документа."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    document_id: uuid.UUID
    is_current: bool
    uploaded_by: Optional[uuid.UUID] = None
    uploaded_at: datetime
