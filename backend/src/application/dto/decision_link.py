"""DTO для связей решений (DecisionLink)."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from backend.src.domain.value_objects.enums import DecisionLinkType


class DecisionLinkBase(BaseModel):
    """Базовые поля для связей решений."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    from_decision_id: uuid.UUID
    to_decision_id: uuid.UUID
    link_type: DecisionLinkType


class DecisionLinkCreate(DecisionLinkBase):
    """DTO для создания связи решений.

    project_id берётся из URL пути.
    """

    pass


class DecisionLinkRead(DecisionLinkBase):
    """DTO для чтения связи решений."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    project_id: uuid.UUID
    created_at: datetime | None = None
