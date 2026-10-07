"""Модель CrossTask (таблица cross_tasks) — ячейка матрицы смежников."""

import uuid

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base, TimestampMixin


class CrossTask(Base, TimestampMixin):
    """Задание смежнику — ячейка матрицы (см. ТЗ 3.0, раздел 4.3)."""

    __tablename__ = "cross_tasks"
    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "from_section_code",
            "to_section_code",
            name="uq_cross_task_project_sections",
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
    from_section_code: Mapped[str] = mapped_column(String(50), nullable=False)
    to_section_code: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="NOT_STARTED")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)