"""DTO для RFI (spec_week_4.md §4)."""

from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from backend.src.domain.value_objects.enums import RfiState, TaskStatus


class RfiBase(BaseModel):
    rfi_cause_decision_id: UUID | None = None
    rfi_cause_goal_id: UUID | None = None
    rfi_due_date: date | None = None
    rfi_state: RfiState | None = RfiState.OPEN
    title: str = Field(
        ..., min_length=1, max_length=1000
    )  # в домене Task поле называется title; formulation — только у эфемерной RfiProposal (6.12b)
    deadline: date | None = None
    assignee_id: UUID | None = None
    is_complex: bool = False


class RfiCreate(RfiBase):
    # project_id передаётся в path-параметре (spec_week_4 §4), не из DTO
    pass


class RfiUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=1000)
    deadline: date | None = None
    assignee_id: UUID | None = None
    is_complex: bool | None = None
    rfi_cause_decision_id: UUID | None = None
    rfi_cause_goal_id: UUID | None = None
    rfi_due_date: date | None = None
    rfi_state: RfiState | None = None


class RfiRead(RfiBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    status: TaskStatus  # в домене Task поле называется status: TaskStatus
    sort_order: int
    source: str
    is_complex: bool
    created_at: datetime
    updated_at: datetime
    premise_ids: list[UUID] = Field(default_factory=list)


class RfiProposal(BaseModel):
    """Эфемерное предложение RFI (не сохраняется в БД)."""

    id: UUID | None = None  # uuid5 для UI-ключей (устанавливается в сервисе)
    action: Literal["create", "escalate"]
    rule: str  # "decision_без_ид" | "rfi_просрочен"
    formulation: str
    rationale: str | None = None
    reason_decision_id: UUID | None = None
    existing_rfi_id: UUID | None = None
    rfi_due_date: date | None = None

    @model_validator(mode="after")
    def _check_action_fields(self):
        if self.action == "create" and self.existing_rfi_id is not None:
            raise ValueError("existing_rfi_id only for escalate")
        if self.action == "escalate" and self.existing_rfi_id is None:
            raise ValueError("existing_rfi_id required for escalate")
        return self


class RfiProposalApprove(BaseModel):
    """Утверждение предложения RFI (action=create)."""

    formulation: str
    rationale: str | None = None
    rfi_cause_decision_id: UUID
    rfi_due_date: date
    rfi_state: RfiState = RfiState.OPEN
