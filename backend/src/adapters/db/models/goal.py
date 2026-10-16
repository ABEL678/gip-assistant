"""Модель Goal (таблица goals)."""

import uuid

from sqlalchemy import Date, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base, TimestampMixin


class GoalModel(Base, TimestampMixin):
    """Цель управления проектом (см. spec_week_1.md, §2)."""

    __tablename__ = "goals"
    __table_args__ = (
        Index("idx_goals_project", "project_id"),
        Index("idx_goals_state", "state"),
        Index("idx_goals_deadline", "deadline"),
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
    formulation: Mapped[str] = mapped_column(String(1000), nullable=False)
    deadline: Mapped[str | None] = mapped_column(Date, nullable=True)
    responsible_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    priority: Mapped[int | None] = mapped_column(Integer, nullable=True)
    state: Mapped[str] = mapped_column(
        String(20), nullable=False, default="plan"
    )
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
