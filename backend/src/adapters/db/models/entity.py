"""Модель Entity (таблица entities)."""

import uuid
from typing import Any

from sqlalchemy import ForeignKey, Index, Integer
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.adapters.db.base import Base, TimestampMixin


class EntityModel(Base, TimestampMixin):
    """Экземпляр пользовательской сущности (см. ТЗ 4.3, раздел 4.4)."""

    __tablename__ = "entities"
    __table_args__ = (
        Index("idx_entities_project", "project_id"),
        Index("idx_entities_type", "entity_type_id"),
        Index("idx_entities_data_gin", "data", postgresql_using="gin"),
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
    entity_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("entity_types.id", ondelete="CASCADE"),
        nullable=False,
    )
    data: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Связи
    entity_type = relationship("EntityTypeModel", back_populates="entities")