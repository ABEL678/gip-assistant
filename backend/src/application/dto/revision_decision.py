"""DTO для RevisionDecision (решение по изменению)."""

import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from backend.src.domain.value_objects.enums import RevisionDecisionType


class RevisionDecisionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    change_id: uuid.UUID
    decision: RevisionDecisionType
    decided_by: Optional[uuid.UUID] = None
    deadline: Optional[date] = None


class RevisionDecisionCreate(RevisionDecisionSchema):
    pass


class RevisionDecisionUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    decision: Optional[RevisionDecisionType] = None
    decided_by: Optional[uuid.UUID] = None
    deadline: Optional[date] = None


class RevisionDecisionRead(RevisionDecisionSchema):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
