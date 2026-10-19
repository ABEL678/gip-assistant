"""Модель Document (таблица documents)."""

import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base, TimestampMixin


class DocumentModel(Base, TimestampMixin):
    """ГОСТ-документ (см. ТЗ 4.4, ГОСТ Р 21.101-2026)."""

    __tablename__ = "documents"
    __table_args__ = (
        Index("idx_documents_project", "project_id"),
        Index("idx_documents_entity", "entity_id"),
        Index("idx_documents_task", "task_id"),
        Index("idx_documents_type", "document_type_id"),
        Index("idx_documents_status", "lifecycle_status"),
        Index("idx_documents_premise", "premise_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    guid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        unique=True,
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    entity_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("entities.id", ondelete="SET NULL"),
        nullable=True,
    )
    task_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="SET NULL"),
        nullable=True,
    )
    premise_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("premises.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Обозначение (ГОСТ Р 21.101-2026, 4.1, 4.2)
    cipher: Mapped[str] = mapped_column(String(500), nullable=False)
    base_designation: Mapped[str | None] = mapped_column(String(200), nullable=True)
    section_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    document_kind: Mapped[str] = mapped_column(String(10), nullable=False, default="ПД")
    mark: Mapped[str | None] = mapped_column(String(50), nullable=True)
    doc_part_type: Mapped[str | None] = mapped_column(String(10), nullable=True)

    # Наименование
    document_name: Mapped[str] = mapped_column(String(500), nullable=False)
    document_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("document_types.id"),
        nullable=False,
    )

    # Версионность (current_version_id — НЕ FK, избегаем циклической зависимости)
    current_version_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    version_parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.id"),
        nullable=True,
    )
    replaces_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.id"),
        nullable=True,
    )
    replaced_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.id"),
        nullable=True,
    )

    # Жизненный цикл
    lifecycle_status: Mapped[str] = mapped_column(String(20), nullable=False, default="DRAFT")

    # Подпись (метаданные)
    signed_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    signed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    signature_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    signature_status: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Служебные
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
