"""DTO для Project."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.src.domain.value_objects.enums import StageType


class ProjectBase(BaseModel):
    """Общие поля проекта."""

    name: str = Field(..., min_length=1, max_length=500)
    code: str = Field(..., min_length=1, max_length=50)
    stage: StageType = StageType.PD
    client: str | None = Field(default=None, max_length=300)
    contract_number: str | None = Field(default=None, max_length=100)


class ProjectCreate(ProjectBase):
    """Создание проекта (POST /api/projects)."""

    pass


class ProjectUpdate(BaseModel):
    """Частичное обновление (PATCH /api/projects/{id})."""

    name: str | None = Field(default=None, min_length=1, max_length=500)
    stage: StageType | None = None
    client: str | None = Field(default=None, max_length=300)
    contract_number: str | None = Field(default=None, max_length=100)


class ProjectRead(ProjectBase):
    """Чтение проекта (GET /api/projects/{id})."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime