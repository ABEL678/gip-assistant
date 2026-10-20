"""Model ProjectStandard (таблица project_standards)."""

import uuid

from sqlalchemy import Enum, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base, TimestampMixin
from backend.src.domain.value_objects.enums import ProjectStandardType


class ProjectStandardModel(Base, TimestampMixin):
    """Стандарт проекта (см. spec_week_1.md, §2.4)."""

    __tablename__ = "project_standards"
    __table_args__ = (
        Index("idx_project_standards_premise", "premise_id"),
        Index("idx_project_standards_type", "type"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    premise_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("premises.id", ondelete="CASCADE"),
        nullable=False,
    )
    type: Mapped[str] = mapped_column(
        Enum(
            ProjectStandardType,
            name="project_standard_type",
            create_type=False,
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
    )
    value: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    approved_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
