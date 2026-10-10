# backend/src/application/dto/entity_type.py
import uuid
from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic import AliasChoices


class FieldDefinition(BaseModel):
    """Описание одного поля в схеме типа сущности."""
    key: str = Field(..., min_length=1, max_length=50)
    label: str = Field(..., min_length=1, max_length=100)
    type: str  # text / number / date / select / multiselect / boolean / textarea / url / email
    required: bool = False
    options: Optional[List[str]] = None
    default: Optional[Any] = None
    description: Optional[str] = None


class EntityTypeSchema(BaseModel):
    """Схема типа сущности (набор полей)."""
    fields: List[FieldDefinition] = Field(default_factory=list)


class EntityTypeBase(BaseModel):
    """Базовые поля для создания/обновления типа."""
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(..., min_length=1, max_length=200)
    icon: str = "📄"
    color: str = "gray"
    description: Optional[str] = None
    schema_: EntityTypeSchema = Field(
        ...,
        validation_alias=AliasChoices("schema", "field_schema"),
        serialization_alias="schema",
    )
    sort_order: int = 0


class EntityTypeCreate(EntityTypeBase):
    """DTO для создания типа сущности.

    project_id НЕ включается — он берётся из URL пути.
    """
    pass


class EntityTypeUpdate(BaseModel):
    """DTO для обновления типа сущности (все поля опциональны)."""
    model_config = ConfigDict(populate_by_name=True)

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    icon: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    schema_: Optional[EntityTypeSchema] = Field(
        None,
        validation_alias=AliasChoices("schema", "field_schema"),
        serialization_alias="schema",
    )
    sort_order: Optional[int] = None


class EntityTypeRead(EntityTypeBase):
    """DTO для чтения типа сущности."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    project_id: uuid.UUID
    is_system: bool
    created_at: datetime
    updated_at: datetime