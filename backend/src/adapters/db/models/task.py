"""Модель Task (таблица tasks)."""

import uuid
from datetime import date

from sqlalchemy import Boolean, CheckConstraint, Date, Enum, ForeignKey, Index, Integer, String, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base, TimestampMixin
from backend.src.domain.value_objects.enums import RfiState


class Task(Base, TimestampMixin):
    """Задача (см. ТЗ 4.3, раздел 4.3)."""

    __tablename__ = "tasks"
    __table_args__ = (
        Index("idx_tasks_project", "project_id"),
        Index("idx_tasks_status", "status"),
        Index("idx_tasks_deadline", "deadline"),
        Index("idx_tasks_section", "section_code"),
        Index("idx_tasks_to_section", "to_section_code"),
        Index("idx_tasks_decision", "decision_id"),
        Index("idx_tasks_rfi_due_date", "rfi_due_date", postgresql_where=text("is_rfi = true")),
        Index("idx_tasks_rfi_cause_decision", "rfi_cause_decision_id", postgresql_where=text("is_rfi = true")),
        Index("idx_tasks_rfi_cause_goal", "rfi_cause_goal_id", postgresql_where=text("is_rfi = true")),
        Index("idx_tasks_is_rfi", "is_rfi", postgresql_where=text("is_rfi = true")),
        CheckConstraint(
            "(is_rfi = false) OR (rfi_cause_decision_id IS NOT NULL OR rfi_cause_goal_id IS NOT NULL)",
            name="ck_tasks_rfi_cause",
        ),
        CheckConstraint(
            "(is_rfi = false AND rfi_state IS NULL) OR (is_rfi = true AND rfi_state IS NOT NULL)",
            name="ck_tasks_rfi_state",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="NOT_STARTED")
    assignee_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("executors.id"),
        nullable=True,
    )
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    section_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    to_section_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    source: Mapped[str] = mapped_column(String(20), nullable=False, default="manual")
    is_complex: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    decision_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("decisions.id", ondelete="SET NULL"),
        nullable=True,
    )
    is_rfi: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    rfi_cause_decision_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("decisions.id", ondelete="SET NULL"),
        nullable=True,
    )
    rfi_cause_goal_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("goals.id", ondelete="SET NULL"),
        nullable=True,
    )
    rfi_due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    rfi_state: Mapped[RfiState | None] = mapped_column(
        Enum(RfiState, name="rfi_state", create_type=False),
        nullable=True,
    )
