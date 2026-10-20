"""Model ResultGoal (таблица result_goals)."""

import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base


class ResultGoalModel(Base):
    """Связь Result ↔ Goal (M:N)."""

    __tablename__ = "result_goals"

    result_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("results.id", ondelete="CASCADE"),
        primary_key=True,
    )
    goal_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("goals.id", ondelete="CASCADE"),
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False,
    )
