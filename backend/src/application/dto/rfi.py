"""DTO для RFI (spec_week_4.md §4)."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from backend.src.domain.value_objects.enums import RfiState, TaskStatus


class RfiBase(BaseModel):
    rfi_cause_decision_id: UUID | None = None
    rfi_cause_goal_id: UUID | None = None
    rfi_due_date: date | None = None
    rfi_state: RfiState | None = RfiState.OPEN
    title: str = Field(..., min_length=1, max_length=1000)  # в домене Task поле называется title; formulation — только у эфемерной RfiProposal (6.12b)
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
