"""DTO для ProjectStandard (spec_week_1.md §2.4)."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from backend.src.domain.value_objects.enums import ProjectStandardType


class ProjectStandardSchema(BaseModel):
    """Базовые поля для ProjectStandard."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    premise_id: uuid.UUID
    type: ProjectStandardType
    value: dict[str, Any] = Field(default_factory=dict)


class ProjectStandardCreate(ProjectStandardSchema):
    """DTO для создания стандарта проекта."""

    pass


class ProjectStandardUpdate(BaseModel):
    """DTO для обновления стандарта проекта (все поля опциональны)."""

    model_config = ConfigDict(populate_by_name=True)

    premise_id: uuid.UUID | None = None
    type: ProjectStandardType | None = None
    value: dict[str, Any] | None = None


class ProjectStandardRead(ProjectStandardSchema):
    """DTO для чтения стандарта проекта."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    approved_by: uuid.UUID | None = None
    created_at: datetime
    updated_at: datetime
