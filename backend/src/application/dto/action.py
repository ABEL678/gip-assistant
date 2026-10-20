"""DTO для действий (Action)."""

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.src.domain.value_objects.enums import ActionState


class ActionSchema(BaseModel):
    """Базовые поля для действий."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    formulation: str = Field(..., min_length=1, max_length=1000)
    task_id: uuid.UUID | None = None
    measurable_result: str | None = Field(None, max_length=1000)
    deadline: date | None = None
    responsible_id: uuid.UUID | None = None
    state: ActionState = ActionState.PLAN


class ActionCreate(ActionSchema):
    """DTO для создания действия.

    project_id берётся из URL пути.
    """

    pass


class ActionUpdate(BaseModel):
    """DTO для обновления действия (все поля опциональны)."""

    model_config = ConfigDict(populate_by_name=True)

    formulation: str | None = Field(None, min_length=1, max_length=1000)
    task_id: uuid.UUID | None = None
    measurable_result: str | None = Field(None, max_length=1000)
    deadline: date | None = None
    responsible_id: uuid.UUID | None = None
    state: ActionState | None = None


class ActionRead(ActionSchema):
    """DTO для чтения действия."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    project_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
