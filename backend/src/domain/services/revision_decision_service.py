"""RevisionDecisionService — бизнес-логика решений по изменениям."""

import logging
from uuid import UUID

from backend.src.domain.entities.revision_decision import RevisionDecision
from backend.src.domain.ports.repositories import RevisionDecisionRepository
from backend.src.domain.value_objects.enums import RevisionDecisionType

logger = logging.getLogger(__name__)


class RevisionDecisionService:
    """Сервис работы с решениями по изменениям (RevisionDecision)."""

    def __init__(self, repo: RevisionDecisionRepository) -> None:
        self._repo = repo

    async def get_by_id(self, decision_id: UUID) -> RevisionDecision | None:
        """Найти решение по ID."""
        return await self._repo.get_by_id(decision_id)

    async def list_by_change(self, change_id: UUID) -> list[RevisionDecision]:
        """Решения по изменению."""
        return await self._repo.list_by_change(change_id)

    async def create(
        self,
        change_id: UUID,
        decision: RevisionDecisionType,
        decided_by: UUID | None = None,
        deadline=None,
    ) -> RevisionDecision:
        """Создать решение по изменению.

        Args:
            change_id: UUID изменения.
            decision: Тип решения.
            decided_by: Кто принял решение.
            deadline: Срок выполнения.
        """
        decision_obj = RevisionDecision(
            change_id=change_id,
            decision=decision,
            decided_by=decided_by,
            deadline=deadline,
        )
        return await self._repo.save(decision_obj)

    async def delete(self, decision_id: UUID) -> None:
        """Удалить решение.

        Raises:
            ValueError: если решение не найдено.
        """
        decision = await self._repo.get_by_id(decision_id)
        if decision is None:
            raise ValueError(f"Решение {decision_id} не найдено")

        await self._repo.delete(decision_id)
