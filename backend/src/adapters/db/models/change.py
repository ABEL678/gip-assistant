"""Модель Change (таблица changes)."""

import uuid

from sqlalchemy import Enum, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base, TimestampMixin
from backend.src.domain.value_objects.enums import ChangeStatus


class ChangeModel(Base, TimestampMixin):
    """Что изменилось между ревизиями (см. DOMAIN.md §3.5)."""

    __tablename__ = "changes"
    __table_args__ = (
        Index("idx_changes_revision", "revision_id"),
        Index("idx_changes_status", "status"),
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
    field: Mapped[str] = mapped_column(String(200), nullable=False)
    old_value: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    new_value: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    status: Mapped[str] = mapped_column(
        Enum(ChangeStatus, name="change_status", create_type=False),
        nullable=False,
    )
