"""DTO для вводных (Premise)."""

import uuid
from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic import AliasChoices

from backend.src.domain.value_objects.enums import PremiseCategory


class PremiseSchema(BaseModel):
    """Базовые поля для вводных."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    category: PremiseCategory
    name: str = Field(..., min_length=1, max_length=500)
    source: Optional[str] = Field(None, max_length=500)
    date: Optional[date] = None
    actual: bool = True
    mandatory: bool = True
    link: Optional[str] = Field(None, max_length=1000)
    valid_until: Optional[date] = None
    data: dict[str, Any] = Field(default_factory=dict)
    field_schema: dict[str, Any] = Field(
        default_factory=dict,
        validation_alias=AliasChoices("schema", "field_schema"),
        serialization_alias="schema",
    )


class PremiseCreate(PremiseSchema):
    """DTO для создания вводной.

    project_id берётся из URL пути.
    """

    pass


class PremiseUpdate(BaseModel):
    """DTO для обновления вводной (все поля опциональны)."""

    model_config = ConfigDict(populate_by_name=True)

    category: Optional[PremiseCategory] = None
    name: Optional[str] = Field(None, min_length=1, max_length=500)
    source: Optional[str] = Field(None, max_length=500)
    date: Optional[date] = None
    actual: Optional[bool] = None
    mandatory: Optional[bool] = None
    link: Optional[str] = Field(None, max_length=1000)
    valid_until: Optional[date] = None
    data: Optional[dict[str, Any]] = None
    field_schema: Optional[dict[str, Any]] = Field(
        None,
        validation_alias=AliasChoices("schema", "field_schema"),
        serialization_alias="schema",
    )


class PremiseRead(PremiseSchema):
    """DTO для чтения вводной."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    project_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
