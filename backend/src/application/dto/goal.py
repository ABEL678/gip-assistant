"""DTO для целей (Goal)."""

import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from backend.src.domain.value_objects.enums import GoalState, VerificationStatus


class GoalSchema(BaseModel):
    """Базовые поля для целей."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    formulation: str = Field(..., min_length=1, max_length=1000)
    deadline: Optional[date] = None
    responsible_id: Optional[uuid.UUID] = None
    priority: Optional[int] = None
    state: GoalState = GoalState.PLAN
    verification_status: VerificationStatus = VerificationStatus.REQUIRES_CHECK
    created_by: Optional[uuid.UUID] = None
    premise_ids: list[uuid.UUID] = Field(default_factory=list)


class GoalCreate(GoalSchema):
    """DTO для создания цели.

    project_id берётся из URL пути.
    """

    pass


class GoalUpdate(BaseModel):
    """DTO для обновления цели (все поля опциональны)."""

    model_config = ConfigDict(populate_by_name=True)

    formulation: Optional[str] = Field(None, min_length=1, max_length=1000)
    deadline: Optional[date] = None
    responsible_id: Optional[uuid.UUID] = None
    priority: Optional[int] = None
    state: Optional[GoalState] = None
    created_by: Optional[uuid.UUID] = None
    premise_ids: Optional[list[uuid.UUID]] = None


class GoalRead(GoalSchema):
    """DTO для чтения цели."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    project_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class GoalProposal(BaseModel):
    """Эфемерная схема для предложения цели системой.

    Используется в GoalProposalService для возврата предложенных целей.
    """

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    formulation: str
    deadline: Optional[date] = None
    priority: Optional[int] = None
    premise_ids: list[uuid.UUID] = Field(default_factory=list)
    verification_status: VerificationStatus = VerificationStatus.REQUIRES_CHECK
    rule: str  # название правила: "договор_срок", "тз_требование", ...
    confidence: float = 1.0  # 1.0 = явное правило, < 1.0 = нужен LLM


# Псевдоним для роутов — GoalProposalRead = GoalProposal
GoalProposalRead = GoalProposal


class GoalProposalApprove(BaseModel):
    """DTO для утверждения предложения цели.

    ГИП может править перед утверждением.
    """

    formulation: str = Field(..., min_length=1, max_length=1000)
    deadline: Optional[date] = None
    priority: Optional[int] = None
    premise_ids: list[uuid.UUID] = Field(default_factory=list)
