"""Доменная сущность Task."""

from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID, uuid4

from backend.src.domain.value_objects.enums import RfiState, TaskStatus


@dataclass
class Task:
    """Задача."""

    project_id: UUID
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.NOT_STARTED
    assignee_id: UUID | None = None
    deadline: date | None = None
    section_code: str | None = None  # от кого (источник задания)
    to_section_code: str | None = None  # кому (получатель задания)
    sort_order: int = 0
    source: str = "manual"
    is_complex: bool = False
    decision_id: UUID | None = None
    is_rfi: bool = False
    rfi_cause_decision_id: UUID | None = None
    rfi_cause_goal_id: UUID | None = None
    rfi_due_date: date | None = None
    rfi_state: RfiState | None = None
    premise_ids: list[UUID] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None
