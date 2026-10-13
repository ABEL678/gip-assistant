"""Модель DocumentVersion (таблица document_versions)."""

import uuid
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base


class DocumentVersionModel(Base):
    """Версия файла ГОСТ-документа."""

    __tablename__ = "document_versions"
    __table_args__ = (
        UniqueConstraint("document_id", "version"),
        Index("idx_document_versions_document", "document_id"),
        Index(
            "idx_document_versions_current",
            "document_id",
            "is_current",
            postgresql_where=text("is_current = TRUE"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    version: Mapped[str] = mapped_column(String(20), nullable=False)
    change_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    file_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    file_name: Mapped[str] = mapped_column(String(500), nullable=False)
    hash_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    format_original: Mapped[str] = mapped_column(String(20), nullable=False)
    format_archive: Mapped[str | None] = mapped_column(String(20), nullable=True)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    uploaded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
