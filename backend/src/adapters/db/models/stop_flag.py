"""Модель StopFlag (таблица stop_flags)."""

import uuid

from sqlalchemy import Boolean, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base, TimestampMixin


class StopFlagModel(Base, TimestampMixin):
    """Стоп-сигнал для ревизии (см. DOMAIN.md §3.5)."""

    __tablename__ = "stop_flags"
    __table_args__ = (
        Index("idx_stop_flags_revision", "revision_id"),
        Index("idx_stop_flags_resolved", "resolved"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    revision_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("revisions.id", ondelete="CASCADE"),
        nullable=False,
    )
    reason: Mapped[str] = mapped_column(String(1000), nullable=False)
    resolved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
