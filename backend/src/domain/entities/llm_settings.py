"""Доменная сущность LLMSettings (настройки LLM-провайдера)."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from backend.src.domain.value_objects.enums import LLMProvider


@dataclass
class LLMSettings:
    """Настройки LLM-провайдера (6.14a).

    Plaintext-ключа в сущности нет: только Fernet-ciphertext и last4.
    """

    provider: LLMProvider
    model_name: str
    base_url: str | None = None
    api_key_encrypted: bytes | None = None
    api_key_last4: str | None = None
    params: dict[str, Any] = field(default_factory=dict)
    is_active: bool = False
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None
