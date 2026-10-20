"""Result entity (spec_week_1.md §2.3)."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Result:
    """Результат проекта (потребительская ценность для Заказчика)."""

    project_id: UUID
    formulation: str
    source: str | None = None
    approved_by: UUID | None = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None
