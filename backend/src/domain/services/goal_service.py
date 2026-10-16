"""GoalService — бизнес-логика целей."""

import logging
from uuid import UUID

from backend.src.domain.entities.goal import Goal
from backend.src.domain.ports.repositories import GoalRepository, PremiseRepository

logger = logging.getLogger(__name__)


class GoalService:
    """Сервис работы с целями (Goal)."""

    def __init__(
        self,
        repo: GoalRepository,
        premise_repo: PremiseRepository,
    ) -> None:
        self._repo = repo
        self._premise_repo = premise_repo

    async def get(self, goal_id: UUID) -> Goal | None:
        """Найти цель по ID."""
        return await self._repo.get_by_id(goal_id)

    async def list_by_project(self, project_id: UUID) -> list[Goal]:
        """Список целей проекта."""
        return await self._repo.list_by_project(project_id)

    async def create(
        self,
        project_id: UUID,
        formulation: str,
        premise_ids: list[UUID] | None = None,
        **kwargs,
    ) -> Goal:
        """Создать цель.

        Args:
            project_id: UUID проекта.
            formulation: Формулировка цели (не пустая).
            premise_ids: Список ID вводных-источников.

        Raises:
            ValueError: если formulation пустое или premise_ids не найдены.
        """
        formulation = formulation.strip()
        if not formulation:
            raise ValueError("Формулировка цели не может быть пустой")

        premise_ids = premise_ids or []
        if premise_ids:
            for pid in premise_ids:
                premise = await self._premise_repo.get_by_id(pid)
                if premise is None:
                    raise ValueError(
                        f"Вводная {pid} не найдена для связи с целью"
                    )

        goal = Goal(
            project_id=project_id,
            formulation=formulation,
            premise_ids=premise_ids,
            **kwargs,
        )
        return await self._repo.save(goal)

    async def update(
        self,
        goal_id: UUID,
        **kwargs,
    ) -> Goal:
        """Обновить цель.

        Args:
            goal_id: UUID цели.

        Raises:
            ValueError: если цель не найдена.
        """
        goal = await self._repo.get_by_id(goal_id)
        if goal is None:
            raise ValueError(f"Цель {goal_id} не найдена")

        # Проверяем premise_ids если они переданы
        if "premise_ids" in kwargs and kwargs["premise_ids"] is not None:
            for pid in kwargs["premise_ids"]:
                premise = await self._premise_repo.get_by_id(pid)
                if premise is None:
                    raise ValueError(
                        f"Вводная {pid} не найдена для связи с целью"
                    )

        for key, value in kwargs.items():
            if value is not None and hasattr(goal, key):
                setattr(goal, key, value)

        return await self._repo.save(goal)

    async def delete(self, goal_id: UUID) -> None:
        """Удалить цель.

        Raises:
            ValueError: если цель не найдена.
        """
        goal = await self._repo.get_by_id(goal_id)
        if goal is None:
            raise ValueError(f"Цель {goal_id} не найдена")

        await self._repo.delete(goal_id)
