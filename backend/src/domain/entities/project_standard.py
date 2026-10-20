"""ProjectStandard entity (spec_week_1.md §2.4)."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from backend.src.domain.value_objects.enums import ProjectStandardType


@dataclass
class ProjectStandard:
    """Стандарт проекта (ограничение для целей)."""

    premise_id: UUID
    type: ProjectStandardType
    value: dict[str, Any] = field(default_factory=dict)
    approved_by: UUID | None = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None
