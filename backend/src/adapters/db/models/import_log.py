"""Модель ImportLog (таблица import_logs)."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base


class ImportLog(Base):
    """Лог импорта Excel (см. ТЗ 4.3, раздел 4.3)."""

    __tablename__ = "import_logs"
    __table_args__ = (
        Index("idx_import_logs_project", "project_id"),
    )
    ...

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id"),
        nullable=False,
    )
    filename: Mapped[str | None] = mapped_column(String(500), nullable=True)
    rows_imported: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rows_failed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="SUCCESS")
    column_mapping: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    error_details: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    imported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )