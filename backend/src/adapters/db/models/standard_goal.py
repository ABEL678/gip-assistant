"""Model StandardGoal (таблица standard_goals)."""

import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base


class StandardGoalModel(Base):
    """Связь ProjectStandard ↔ Goal (M:N)."""

    __tablename__ = "standard_goals"

    standard_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("project_standards.id", ondelete="CASCADE"),
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
