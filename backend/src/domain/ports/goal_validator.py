"""Порт GoalValidator — интерфейс агента-валидатора (DOMAIN.md §4.4.1)."""

from abc import ABC, abstractmethod
from uuid import UUID

from backend.src.application.dto.validation_result import ValidationResult


class GoalValidatorService(ABC):
    """Интерфейс валидатора Goal.

    Реализации:
    - RuleBasedGoalValidator — правила 1–6 (веха 1–5, детерминированный).
    - LLMGoalValidator — веха 6 (недетерминированный).
    """

    @abstractmethod
    async def validate(self, goal_id: UUID) -> ValidationResult: ...
