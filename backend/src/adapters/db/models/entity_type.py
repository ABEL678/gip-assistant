"""Модель EntityType (таблица entity_types)."""

import uuid
from typing import Any

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.adapters.db.base import Base, TimestampMixin


class EntityTypeModel(Base, TimestampMixin):
    """Тип пользовательской сущности (см. ТЗ 4.3, раздел 4.4)."""

    __tablename__ = "entity_types"
    __table_args__ = (
        Index("idx_entity_types_project", "project_id"),
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
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    icon: Mapped[str] = mapped_column(String(50), nullable=False, default="📄")
    color: Mapped[str] = mapped_column(String(20), nullable=False, default="gray")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    schema: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    xml_schema_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_system: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Связи
    entities = relationship(
        "EntityModel",
        back_populates="entity_type",
        cascade="all, delete-orphan",
    )