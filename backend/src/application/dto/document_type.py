"""DTO для типов ГОСТ-документов."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DocumentTypeBase(BaseModel):
    """Базовые поля для типов ГОСТ-документов."""
    code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    gost_code: Optional[str] = Field(None, max_length=50)


class DocumentTypeCreate(DocumentTypeBase):
    """DTO для создания типа ГОСТ-документа."""
    pass


class DocumentTypeUpdate(BaseModel):
    """DTO для обновления типа ГОСТ-документа (все поля опциональны)."""
    model_config = ConfigDict(populate_by_name=True)

    name: Optional[str] = Field(None, min_length=1, max_length=200)  # noqa: UP045
    description: Optional[str] = None  # noqa: UP045
    gost_code: Optional[str] = Field(None, max_length=50)  # noqa: UP045


class DocumentTypeRead(DocumentTypeBase):
    """DTO для чтения типа ГОСТ-документа."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    created_at: datetime
