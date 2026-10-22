"""DTO для нормативных документов (Norm)."""

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.src.domain.value_objects.enums import NormType


class NormBase(BaseModel):
    """Базовые поля для норм."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    code: str = Field(..., max_length=100)
    title: str = Field(..., max_length=500)
    norm_type: NormType
    issued_at: date | None = None
    source_url: str | None = Field(None, max_length=1000)
    document_id: uuid.UUID | None = None


class NormCreate(NormBase):
    """DTO для создания нормы.

    project_id берётся из URL пути.
    """

    pass


class NormUpdate(BaseModel):
    """DTO для обновления нормы (все поля опциональны)."""

    model_config = ConfigDict(populate_by_name=True)

    code: str | None = Field(None, max_length=100)
    title: str | None = Field(None, max_length=500)
    norm_type: NormType | None = None
    issued_at: date | None = None
    source_url: str | None = Field(None, max_length=1000)
    document_id: uuid.UUID | None = None


class NormRead(NormBase):
    """DTO для чтения нормы."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    project_id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None
