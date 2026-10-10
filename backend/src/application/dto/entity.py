# backend/src/application/dto/entity.py
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class EntityBase(BaseModel):
    """Базовые поля для сущности."""
    data: Dict[str, Any] = Field(default_factory=dict)
    sort_order: int = 0


class EntityCreate(EntityBase):
    """DTO для создания записи сущности.

    entity_type_id НЕ включается — берётся из URL.
    project_id нужен для привязки.
    """
    project_id: uuid.UUID


class EntityUpdate(BaseModel):
    """DTO для обновления записи сущности."""
    data: Optional[Dict[str, Any]] = None
    sort_order: Optional[int] = None


class EntityRead(EntityBase):
    """DTO для чтения записи сущности."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    entity_type_id: uuid.UUID
    created_at: datetime
    updated_at: datetime