"""Модель Revision (таблица revisions)."""

import uuid
from datetime import date as date_type

from sqlalchemy import Boolean, Date, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base, TimestampMixin


class RevisionModel(Base, TimestampMixin):
    """Версия документа (см. DOMAIN.md §3.5)."""

    __tablename__ = "revisions"
    __table_args__ = (
        Index("idx_revisions_document", "document_id"),
        Index("idx_revisions_date", "date"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[date_type | None] = mapped_column(Date, nullable=True)
    source: Mapped[str | None] = mapped_column(String(500), nullable=True)
    notified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    stop_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
