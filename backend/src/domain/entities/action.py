"""Доменная сущность Action (Действие)."""

from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID, uuid4

from backend.src.domain.value_objects.enums import ActionState


@dataclass
class Action:
    """Действие — атомарная единица работы.

    Args:
        project_id: UUID проекта.
        formulation: Формулировка действия.

    Kwargs:
        task_id: Связанная задача (nullable — Action может существовать вне Task).
        measurable_result: Измеримый результат.
        deadline: Срок выполнения.
        responsible_id: Ответственный.
        state: Состояние (по умолчанию PLAN).
        id: UUID действия.
        created_at: Дата создания.
        updated_at: Дата обновления.
    """

    # Обязательные (без default)
    project_id: UUID
    formulation: str

    # Опциональные (с default)
    task_id: UUID | None = None
    measurable_result: str | None = None
    deadline: date | None = None
    responsible_id: UUID | None = None
    state: ActionState = ActionState.PLAN
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None
