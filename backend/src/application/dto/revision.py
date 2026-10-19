"""DTO для Revision (версия документа)."""

import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RevisionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    document_id: uuid.UUID
    version: int = Field(..., ge=1)
    date: Optional[date] = None
    source: Optional[str] = Field(None, max_length=500)
    notified: bool = False
    stop_flag: bool = False


class RevisionCreate(RevisionSchema):
    pass


class RevisionUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    version: Optional[int] = Field(None, ge=1)
    date: Optional[date] = None
    source: Optional[str] = Field(None, max_length=500)
    notified: Optional[bool] = None
    stop_flag: Optional[bool] = None


class RevisionRead(RevisionSchema):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
