"""Доменная сущность RevisionDecision (решение по изменению)."""

from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID, uuid4

from backend.src.domain.value_objects.enums import RevisionDecisionType


@dataclass
class RevisionDecision:
    """Решение ГИП по изменению между ревизиями."""

    # Обязательные
    change_id: UUID
    decision: RevisionDecisionType

    # Опциональные
    decided_by: UUID | None = None
    deadline: date | None = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None
