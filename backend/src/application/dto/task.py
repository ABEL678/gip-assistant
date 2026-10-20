"""DTO для Task."""

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.src.domain.value_objects.enums import TaskStatus


class TaskBase(BaseModel):
    """Общие поля задачи."""

    title: str = Field(..., min_length=1, max_length=500)
    description: str | None = None
    deadline: date | None = None
    section_code: str | None = Field(default=None, max_length=50)
    to_section_code: str | None = Field(default=None, max_length=50)
    assignee_id: uuid.UUID | None = None
    is_complex: bool = False


class TaskCreate(TaskBase):
    """Создание задачи (POST /api/projects/{id}/tasks)."""

    project_id: uuid.UUID


class TaskUpdate(BaseModel):
    """Частичное обновление (PATCH /api/tasks/{id})."""

    title: str | None = Field(default=None, min_length=1, max_length=500)
    description: str | None = None
    status: TaskStatus | None = None
    deadline: date | None = None
    section_code: str | None = Field(default=None, max_length=50)
    to_section_code: str | None = Field(default=None, max_length=50)
    assignee_id: uuid.UUID | None = None
    sort_order: int | None = None
    is_complex: bool | None = None


class TaskRead(TaskBase):
    """Чтение задачи (GET /api/tasks/{id})."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    status: TaskStatus
    sort_order: int
    source: str
    is_complex: bool
    created_at: datetime
    updated_at: datetime


class CrossTaskTaskRead(TaskRead):
    """Задача в контексте пары матрицы (с вычисленной просрочкой)."""

    overdue_days: int = Field(
        default=0,
        description="Сколько дней просрочена (0 если не просрочена)",
    )
    days_until_deadline: int | None = Field(
        default=None,
        description="Сколько дней до дедлайна (отрицательно если просрочено)",
    )
