"""Модель LLMSettings (таблица llm_settings, 6.14a)."""

import uuid
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Enum,
    Index,
    LargeBinary,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base, TimestampMixin
from backend.src.domain.value_objects.enums import LLMProvider


class LLMSettingsModel(Base, TimestampMixin):
    """Настройки LLM-провайдера (6.14a)."""

    __tablename__ = "llm_settings"
    __table_args__ = (
        CheckConstraint(
            "(api_key_encrypted IS NULL) = (api_key_last4 IS NULL)",
            name="ck_llm_settings_key_pair",
        ),
        Index(
            "idx_llm_settings_active",
            "is_active",
            unique=True,
            postgresql_where=text("is_active = true"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    provider: Mapped[LLMProvider] = mapped_column(
        Enum(
            LLMProvider,
            name="llm_provider",
            create_type=False,
            values_callable=lambda e: [x.value for x in e],
        ),
        nullable=False,
    )
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    base_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    api_key_encrypted: Mapped[bytes | None] = mapped_column(
        LargeBinary, nullable=True
    )
    api_key_last4: Mapped[str | None] = mapped_column(String(4), nullable=True)
    params: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
    )
