"""DTO для User."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from backend.src.domain.value_objects.enums import UserRole


class UserBase(BaseModel):
    """Общие поля пользователя."""

    name: str = Field(..., min_length=1, max_length=300)
    role: UserRole = UserRole.DESIGNER
    email: EmailStr | None = None
    telegram_id: int | None = None


class UserCreate(UserBase):
    """Создание пользователя (POST /api/users)."""

    pass


class UserRead(UserBase):
    """Чтение (GET /api/users/{id})."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    is_active: bool
    created_at: datetime