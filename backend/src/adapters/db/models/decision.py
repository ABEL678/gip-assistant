"""Модель Decision (таблица decisions)."""

import uuid

from sqlalchemy import Date, Enum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base, TimestampMixin
from backend.src.domain.value_objects.enums import DecisionState


class DecisionModel(Base, TimestampMixin):
    """Решение управления проектом (см. spec_week_3.md, §2.1)."""

    __tablename__ = "decisions"
    __table_args__ = (
        Index("idx_decisions_project", "project_id"),
        Index("idx_decisions_state", "state"),
        Index("idx_decisions_deadline", "deadline"),
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
    formulation: Mapped[str] = mapped_column(String(500), nullable=False)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    context: Mapped[str | None] = mapped_column(Text, nullable=True)
    deadline: Mapped[str | None] = mapped_column(Date, nullable=True)
    state: Mapped[str] = mapped_column(
        Enum(DecisionState, name="decision_state", create_type=False),
        nullable=False,
        default=DecisionState.PLAN,
    )
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
