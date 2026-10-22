"""Доменная сущность DecisionProposal (предложение решения).

Эфемерная схема для предложений системы (не сохраняется в БД).
Используется DecisionProposalService и API-слоем.
"""

from dataclasses import dataclass, field
from uuid import UUID

from backend.src.domain.value_objects.enums import DecisionState


@dataclass
class DecisionProposal:
    """Предложение решения от системы.

    Args:
        formulation: Формулировка решения.
        rule: Название правила, которое сработало.

    Kwargs:
        rationale: Обоснование.
        state: Состояние предложения (по умолчанию PLAN).
        premise_ids: Какие вводные стали источником.
        goal_ids: К каким целям ведёт решение.
        id: UUID (генерируется в сервисе для UI key).
    """

    formulation: str
    rule: str  # "goal_без_решения", "срок_из_вводных"
    rationale: str | None = None
    state: DecisionState = DecisionState.PLAN
    premise_ids: list[UUID] = field(default_factory=list)
    goal_ids: list[UUID] = field(default_factory=list)
    id: UUID | None = None
