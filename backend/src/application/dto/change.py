"""DTO для Change (изменение между ревизиями)."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from backend.src.domain.value_objects.enums import ChangeStatus


class ChangeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    revision_id: uuid.UUID
    field: str = Field(..., min_length=1, max_length=200)
    old_value: Optional[str] = Field(None, max_length=1000)
    new_value: Optional[str] = Field(None, max_length=1000)
    status: ChangeStatus


class ChangeCreate(ChangeSchema):
    pass


class ChangeUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    field: Optional[str] = Field(None, min_length=1, max_length=200)
    old_value: Optional[str] = Field(None, max_length=1000)
    new_value: Optional[str] = Field(None, max_length=1000)
    status: Optional[ChangeStatus] = None


class ChangeRead(ChangeSchema):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
