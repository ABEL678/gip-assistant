"""DecisionNormService — бизнес-логика связи Decision ↔ Norm (M:N).

Дополнение к spec_week_3.md §6 (по DOMAIN.md §7.2): Norm — отдельная
сущность, связь с Decision через decision_norms.
"""

import logging
from uuid import UUID

from backend.src.domain.ports.repositories import (
    DecisionNormRepository,
    DecisionRepository,
    NormRepository,
)

logger = logging.getLogger(__name__)


class DecisionNormService:
    """Сервис связи решений с нормами (Decision ↔ Norm)."""

    def __init__(
        self,
        repo: DecisionNormRepository,
        decision_repo: DecisionRepository,
        norm_repo: NormRepository,
    ) -> None:
        self._repo = repo
        self._decision_repo = decision_repo
        self._norm_repo = norm_repo

    async def link(self, decision_id: UUID, norm_id: UUID) -> None:
        """Связать решение с нормой.

        Идемпотентно: повторная связь — не ошибка
        (ON CONFLICT DO NOTHING на уровне репозитория).

        Raises:
            ValueError: если решение или норма не найдены,
                или они из разных проектов.
        """
        decision = await self._decision_repo.get_by_id(decision_id)
        if decision is None:
            raise ValueError(f"Решение {decision_id} не найдено")

        norm = await self._norm_repo.get_by_id(norm_id)
        if norm is None:
            raise ValueError(f"Норма {norm_id} не найдена")

        if UUID(str(decision.project_id)) != UUID(str(norm.project_id)):
            raise ValueError(
                "Нельзя связать решение и норму из разных проектов: "
                f"{decision.project_id} vs {norm.project_id}"
            )

        await self._repo.link(decision_id, norm_id)

    async def unlink(self, decision_id: UUID, norm_id: UUID) -> None:
        """Разорвать связь решения с нормой (идемпотентно)."""
        await self._repo.unlink(decision_id, norm_id)

    async def list_norms_by_decision(self, decision_id: UUID) -> list[UUID]:
        """UUID норм, связанных с решением."""
        return await self._repo.list_norms_by_decision(decision_id)

    async def list_decisions_by_norm(self, norm_id: UUID) -> list[UUID]:
        """UUID решений, связанных с нормой."""
        return await self._repo.list_decisions_by_norm(norm_id)
