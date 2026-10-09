"""Доменная сущность User."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from backend.src.domain.value_objects.enums import UserRole


@dataclass
class User:
    """Пользователь."""

    name: str
    role: UserRole = UserRole.DESIGNER
    email: str | None = None
    telegram_id: int | None = None
    is_active: bool = True
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None