"""Доменная сущность Project (не зависит от SQLAlchemy)."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from backend.src.domain.value_objects.enums import StageType


@dataclass
class Project:
    """Проект."""

    name: str
    code: str
    stage: StageType = StageType.PD
    client: str | None = None
    contract_number: str | None = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None