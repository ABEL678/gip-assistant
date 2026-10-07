"""Модель Project (таблица projects)."""

import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base, TimestampMixin


class Project(Base, TimestampMixin):
    """Проект (см. ТЗ 3.0, раздел 4.3)."""

    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    stage: Mapped[str] = mapped_column(String(10), nullable=False, default="PD")
    client: Mapped[str | None] = mapped_column(String(300), nullable=True)
    contract_number: Mapped[str | None] = mapped_column(String(100), nullable=True)