"""Доменная сущность CrossTask (ячейка матрицы смежников)."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from backend.src.domain.value_objects.enums import CrossTaskStatus


@dataclass
class CrossTask:
    """Задание смежнику — ячейка матрицы."""

    project_id: UUID
    from_section_code: str
    to_section_code: str
    status: CrossTaskStatus = CrossTaskStatus.NOT_STARTED
    description: str | None = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None