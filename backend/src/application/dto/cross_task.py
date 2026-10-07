"""DTO для CrossTask (ячейка матрицы смежников)."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.src.domain.value_objects.enums import CrossTaskStatus


class CrossTaskBase(BaseModel):
    """Общие поля задания смежнику."""

    from_section_code: str = Field(..., min_length=1, max_length=50)
    to_section_code: str = Field(..., min_length=1, max_length=50)
    description: str | None = None


class CrossTaskUpdate(BaseModel):
    """Обновление (PATCH /api/cross-tasks/{id})."""

    status: CrossTaskStatus | None = None
    description: str | None = None


class CrossTaskRead(CrossTaskBase):
    """Чтение (GET /api/cross-tasks/{id})."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    status: CrossTaskStatus
    created_at: datetime
    updated_at: datetime