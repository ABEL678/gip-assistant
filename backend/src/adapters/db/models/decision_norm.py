"""Модель DecisionNorm (ассоциативная таблица decision_norms)."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base


class DecisionNormModel(Base):
    """Ассоциативная таблица связи Decision и Norm (M:N)."""

    __tablename__ = "decision_norms"
    __table_args__ = (
        Index("idx_decision_norms_decision", "decision_id"),
        Index("idx_decision_norms_norm", "norm_id"),
    )

    decision_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("decisions.id", ondelete="CASCADE"),
        primary_key=True,
    )
    norm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("norms.id", ondelete="CASCADE"),
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
