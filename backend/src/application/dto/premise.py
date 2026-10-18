"""DTO для вводных (Premise)."""

import uuid
from datetime import date as _date, datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic import AliasChoices

from backend.src.domain.value_objects.enums import PremiseCategory


class PremiseDataField(BaseModel):
    """Поле data вводной с владельцем (DOMAIN.md §3.4.1).

    Если owner не указан — это «нет данных» (нельзя проверить).
    """

    model_config = ConfigDict(populate_by_name=True)

    value: Any
    owner: Optional[str] = None
    source: Optional[str] = None


class PremiseSchema(BaseModel):
    """Базовые поля для вводных."""

    model_config = ConfigDict(populate_by_name=True)

    category: PremiseCategory
    name: str = Field(..., min_length=1, max_length=500)
    source: Optional[str] = Field(None, max_length=500)
    date: Optional[_date] = None
    actual: bool = True
    mandatory: bool = True
    link: Optional[str] = Field(None, max_length=1000)
    valid_until: Optional[_date] = None
    data: dict[str, PremiseDataField] = Field(default_factory=dict)
    schema_: dict[str, Any] = Field(
        default_factory=dict,
        validation_alias=AliasChoices("schema", "field_schema"),
        serialization_alias="schema",
    )

    @field_validator("data", mode="before")
    @classmethod
    def _coerce_plain_values(cls, v: Any) -> Any:
        if not isinstance(v, dict):
            return v
        return {
            k: val if isinstance(val, dict) and "value" in val
            else {"value": val, "owner": None, "source": None}
            for k, val in v.items()
        }


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
    date: Optional[_date] = None
    actual: Optional[bool] = None
    mandatory: Optional[bool] = None
    link: Optional[str] = Field(None, max_length=1000)
    valid_until: Optional[_date] = None
    data: Optional[dict[str, Any]] = None
    schema_: Optional[dict[str, Any]] = Field(
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
