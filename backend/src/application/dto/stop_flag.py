"""DTO для StopFlag (стоп-сигнал)."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class StopFlagSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    revision_id: uuid.UUID
    reason: str = Field(..., min_length=1, max_length=1000)
    resolved: bool = False


class StopFlagCreate(StopFlagSchema):
    pass


class StopFlagUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    reason: Optional[str] = Field(None, min_length=1, max_length=1000)
    resolved: Optional[bool] = None


class StopFlagRead(StopFlagSchema):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
