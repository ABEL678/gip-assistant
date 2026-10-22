"""Доменная сущность Decision (Решение)."""

from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID, uuid4

from backend.src.domain.value_objects.enums import DecisionState


@dataclass
class Decision:
    """Решение управления проектом.

    Args:
        project_id: UUID проекта.
        formulation: Формулировка решения.

    Kwargs:
        rationale: Обоснование.
        context: Контекст.
        deadline: Срок.
        state: Состояние (по умолчанию PLAN).
        created_by: Кто создал.
        premise_ids: Список ID вводных, ставших источником.
        goal_ids: Список ID целей, к которым ведёт решение.
        id: UUID решения.
        created_at: Дата создания.
        updated_at: Дата обновления.
    """

    # Обязательные (без default)
    project_id: UUID
    formulation: str

    # Опциональные (с default)
    rationale: str | None = None
    context: str | None = None
    deadline: date | None = None
    state: DecisionState = DecisionState.PLAN
    created_by: UUID | None = None
    premise_ids: list[UUID] = field(default_factory=list)
    goal_ids: list[UUID] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None
