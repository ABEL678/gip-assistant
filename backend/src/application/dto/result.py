"""DTO для Result (spec_week_1.md §2.3)."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ResultSchema(BaseModel):
    """Базовые поля для Result."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    formulation: str = Field(..., min_length=1, max_length=1000)
    source: str | None = Field(None, max_length=500)


class ResultCreate(ResultSchema):
    """DTO для создания результата."""

    pass


class ResultUpdate(BaseModel):
    """DTO для обновления результата (все поля опциональны)."""

    model_config = ConfigDict(populate_by_name=True)

    formulation: str | None = Field(None, min_length=1, max_length=1000)
    source: str | None = Field(None, max_length=500)


class ResultRead(ResultSchema):
    """DTO для чтения результата."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    project_id: uuid.UUID
    approved_by: uuid.UUID | None = None
    created_at: datetime
    updated_at: datetime
