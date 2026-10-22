"""Модель связи Decision ↔ Goal (таблица decision_goals)."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base


class DecisionGoalModel(Base):
    """Ассоциативная таблица связи Decision и Goal (M:N)."""

    __tablename__ = "decision_goals"
    __table_args__ = (
        Index("idx_decision_goals_decision", "decision_id"),
        Index("idx_decision_goals_goal", "goal_id"),
    )

    decision_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("decisions.id", ondelete="CASCADE"),
        primary_key=True,
    )
    goal_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("goals.id", ondelete="CASCADE"),
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
