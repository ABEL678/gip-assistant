"""Модель DecisionLink (таблица decision_links)."""

import uuid

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base, TimestampMixin
from backend.src.domain.value_objects.enums import DecisionLinkType


class DecisionLinkModel(Base, TimestampMixin):
    """Связь между решениями (см. spec_week_3.md, §2.3)."""

    __tablename__ = "decision_links"
    __table_args__ = (
        Index("idx_decision_links_from", "from_decision_id"),
        Index("idx_decision_links_to", "to_decision_id"),
        UniqueConstraint(
            "from_decision_id", "to_decision_id", "link_type",
            name="uq_decision_links_triple",
        ),
        CheckConstraint(
            "from_decision_id != to_decision_id",
            name="ck_decision_links_no_self",
        ),
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
    from_decision_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("decisions.id", ondelete="CASCADE"),
        nullable=False,
    )
    to_decision_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("decisions.id", ondelete="CASCADE"),
        nullable=False,
    )
    link_type: Mapped[str] = mapped_column(
        Enum(DecisionLinkType, name="decision_link_type", create_type=False),
        nullable=False,
    )
