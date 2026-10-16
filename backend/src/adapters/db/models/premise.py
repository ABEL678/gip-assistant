"""Модель Premise (таблица premises)."""

import uuid
from datetime import date as date_type

from sqlalchemy import Boolean, Date, Enum, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base, TimestampMixin
from backend.src.domain.value_objects.enums import PremiseCategory


class PremiseModel(Base, TimestampMixin):
    """Вводная проекта (см. spec_week_1.md, §2)."""

    __tablename__ = "premises"
    __table_args__ = (
        Index("idx_premises_project", "project_id"),
        Index("idx_premises_category", "category"),
        Index("idx_premises_actual", "actual"),
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
    category: Mapped[str] = mapped_column(
        Enum(PremiseCategory, name="premise_category", create_type=False),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    source: Mapped[str | None] = mapped_column(String(500), nullable=True)
    date: Mapped[date_type | None] = mapped_column(Date, nullable=True)
    actual: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    mandatory: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    link: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    valid_until: Mapped[date_type | None] = mapped_column(Date, nullable=True)
    data: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    schema: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
