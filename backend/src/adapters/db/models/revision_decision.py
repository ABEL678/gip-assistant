"""Модель RevisionDecision (таблица revision_decisions)."""

import uuid
from datetime import date as date_type

from sqlalchemy import Date, Enum, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base, TimestampMixin
from backend.src.domain.value_objects.enums import RevisionDecisionType


class RevisionDecisionModel(Base, TimestampMixin):
    """Решение ГИП по изменению (см. DOMAIN.md §3.5)."""

    __tablename__ = "revision_decisions"
    __table_args__ = (Index("idx_revision_decisions_change", "change_id"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    change_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("changes.id", ondelete="CASCADE"),
        nullable=False,
    )
    decision: Mapped[str] = mapped_column(
        Enum(
            RevisionDecisionType,
            name="revision_decision_type",
            create_type=False,
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
    )
    decided_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    deadline: Mapped[date_type | None] = mapped_column(Date, nullable=True)
