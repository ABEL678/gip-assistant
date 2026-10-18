"""Доменная сущность Goal (Цель)."""

from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID, uuid4

from backend.src.domain.value_objects.enums import GoalState, VerificationStatus


@dataclass
class Goal:
    """Цель управления проектом.

    verification_status: статус проверки (DOMAIN.md §4.4.1).

    Args:
        project_id: UUID проекта.
        formulation: Формулировка цели.

    Kwargs:
        deadline: Срок достижения.
        responsible_id: Ответственный.
        priority: Приоритет (1–5).
        state: Состояние (по умолчанию PLAN).
        created_by: Кто создал.
        premise_ids: Список ID вводных, ставших источником.
        id: UUID цели.
        created_at: Дата создания.
        updated_at: Дата обновления.
    """

    # Обязательные (без default)
    project_id: UUID
    formulation: str

    # Опциональные (с default)
    deadline: date | None = None
    responsible_id: UUID | None = None
    priority: int | None = None
    state: GoalState = GoalState.PLAN
    verification_status: VerificationStatus = VerificationStatus.REQUIRES_CHECK
    created_by: UUID | None = None
    premise_ids: list[UUID] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None
