"""Модель Norm (таблица norms)."""

import uuid
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base, TimestampMixin
from backend.src.domain.value_objects.enums import NormType


class NormModel(Base, TimestampMixin):
    """Нормативный документ (см. spec_week_3.md, §2.2)."""

    __tablename__ = "norms"
    __table_args__ = (
        Index("idx_norms_project", "project_id"),
        Index("idx_norms_type", "norm_type"),
        UniqueConstraint("project_id", "code", name="uq_norms_project_code"),
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
    code: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    norm_type: Mapped[str] = mapped_column(
        Enum(NormType, name="norm_type", create_type=False),
        nullable=False,
    )
    issued_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="SET NULL"),
        nullable=True,
    )
