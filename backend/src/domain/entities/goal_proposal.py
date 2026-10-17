"""Доменная сущность GoalProposal (предложение цели).

Эфемерная схема для предложений системы (не сохраняется в БД).
Используется GoalProposalService и API-слоем.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID


@dataclass
class GoalProposal:
    """Предложение цели от системы.

    Args:
        formulation: Формулировка цели.
        rule: Название правила, которое сработало.

    Kwargs:
        deadline: Срок (опционально).
        priority: Приоритет (опционально).
        premise_ids: Какие вводные стали источником.
        confidence: Уверенность правила (0.0–1.0).
    """

    formulation: str
    rule: str  # "договор_срок", "тз_требование", ...
    deadline: Optional[date] = None
    priority: Optional[int] = None
    premise_ids: list[UUID] = field(default_factory=list)
    confidence: float = 1.0
    id: Optional[UUID] = None  # генерируется в сервисе для UI key
