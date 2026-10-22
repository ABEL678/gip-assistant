"""Модель связи Decision ↔ Premise (таблица decision_premises)."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base


class DecisionPremiseModel(Base):
    """Ассоциативная таблица связи Decision и Premise (M:N)."""

    __tablename__ = "decision_premises"
    __table_args__ = (
        Index("idx_decision_premises_decision", "decision_id"),
        Index("idx_decision_premises_premise", "premise_id"),
    )

    decision_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("decisions.id", ondelete="CASCADE"),
        primary_key=True,
    )
    premise_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("premises.id", ondelete="CASCADE"),
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
