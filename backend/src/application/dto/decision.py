"""DTO для решений (Decision)."""

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.src.domain.value_objects.enums import DecisionState


class DecisionBase(BaseModel):
    """Базовые поля для решений."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    formulation: str = Field(..., min_length=1, max_length=500)
    rationale: str | None = None
    context: str | None = None
    deadline: date | None = None
    state: DecisionState = DecisionState.PLAN
    premise_ids: list[uuid.UUID] = Field(default_factory=list)
    goal_ids: list[uuid.UUID] = Field(default_factory=list)


class DecisionCreate(DecisionBase):
    """DTO для создания решения.

    project_id берется из URL пути.
    """

    pass


class DecisionUpdate(BaseModel):
    """DTO для обновления решения (все поля опциональны)."""

    model_config = ConfigDict(populate_by_name=True)

    formulation: str | None = Field(None, min_length=1, max_length=500)
    rationale: str | None = None
    context: str | None = None
    deadline: date | None = None
    state: DecisionState | None = None
    premise_ids: list[uuid.UUID] | None = None
    goal_ids: list[uuid.UUID] | None = None


class DecisionRead(DecisionBase):
    """DTO для чтения решения."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    project_id: uuid.UUID
    created_by: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class DecisionProposal(BaseModel):
    """Эфемерная схема для предложения решения системой.

    Используется в DecisionProposalService для возврата предложенных решений.
    Не сохраняется в БД.
    """

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    formulation: str
    rationale: str | None = None
    state: DecisionState = DecisionState.PLAN
    premise_ids: list[uuid.UUID] = Field(default_factory=list)
    goal_ids: list[uuid.UUID] = Field(default_factory=list)
    rule: str  # название правила: "goal_без_решения", "срок_из_вводных"
