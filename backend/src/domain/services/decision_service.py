"""DecisionService — бизнес-логика решений."""

import logging
from uuid import UUID

from backend.src.domain.entities.decision import Decision
from backend.src.domain.ports.repositories import (
    DecisionRepository,
    GoalRepository,
    PremiseRepository,
    ProjectRepository,
)
from backend.src.domain.value_objects.enums import DecisionState

logger = logging.getLogger(__name__)


class DecisionService:
    """Сервис работы с решениями (Decision)."""

    def __init__(
        self,
        repo: DecisionRepository,
        project_repo: ProjectRepository,
        premise_repo: PremiseRepository,
        goal_repo: GoalRepository,
    ) -> None:
        self._repo = repo
        self._project_repo = project_repo
        self._premise_repo = premise_repo
        self._goal_repo = goal_repo

    async def get(self, decision_id: UUID) -> Decision | None:
        """Найти решение по ID."""
        return await self._repo.get_by_id(decision_id)

    async def list_by_project(self, project_id: UUID) -> list[Decision]:
        """Список решений проекта."""
        return await self._repo.list_by_project(project_id)

    async def create(
        self,
        project_id: UUID,
        formulation: str,
        premise_ids: list[UUID] | None = None,
        goal_ids: list[UUID] | None = None,
        **kwargs,
    ) -> Decision:
        """Создать решение.

        Args:
            project_id: UUID проекта.
            formulation: Формулировка решения (не пустая).
            premise_ids: Список ID вводных-источников.
            goal_ids: Список ID целей, к которым ведёт решение.

        Raises:
            ValueError: если formulation пустая, проект не найден,
                premise_ids/goal_ids не найдены или из другого проекта,
                state недопустим.
        """
        formulation = formulation.strip()
        if not formulation:
            raise ValueError("Формулировка решения не может быть пустой")

        project = await self._project_repo.get_by_id(project_id)
        if project is None:
            raise ValueError(f"Проект {project_id} не найден")

        state = kwargs.get("state")
        if state is not None and state not in list(DecisionState):
            raise ValueError(f"Недопустимое состояние решения: {state}")

        premise_ids = premise_ids or []
        goal_ids = goal_ids or []
        await self._validate_premise_ids(project_id, premise_ids)
        await self._validate_goal_ids(project_id, goal_ids)

        decision = Decision(
            project_id=project_id,
            formulation=formulation,
            premise_ids=premise_ids,
            goal_ids=goal_ids,
            **kwargs,
        )
        return await self._repo.save(decision)

    async def update(
        self,
        decision_id: UUID,
        **kwargs,
    ) -> Decision:
        """Обновить решение.

        Args:
            decision_id: UUID решения.

        Raises:
            ValueError: если решение не найдено, переданы несуществующие
                premise_ids/goal_ids из другого проекта или недопустимый state.
        """
        decision = await self._repo.get_by_id(decision_id)
        if decision is None:
            raise ValueError(f"Решение {decision_id} не найдено")

        state = kwargs.get("state")
        if state is not None and state not in list(DecisionState):
            raise ValueError(f"Недопустимое состояние решения: {state}")

        if "premise_ids" in kwargs and kwargs["premise_ids"] is not None:
            await self._validate_premise_ids(decision.project_id, kwargs["premise_ids"])
        if "goal_ids" in kwargs and kwargs["goal_ids"] is not None:
            await self._validate_goal_ids(decision.project_id, kwargs["goal_ids"])

        for key, value in kwargs.items():
            if value is not None and hasattr(decision, key):
                setattr(decision, key, value)

        return await self._repo.save(decision)

    async def delete(self, decision_id: UUID) -> None:
        """Удалить решение.

        Raises:
            ValueError: если решение не найдено.
        """
        decision = await self._repo.get_by_id(decision_id)
        if decision is None:
            raise ValueError(f"Решение {decision_id} не найдено")

        await self._repo.delete(decision_id)

    # ---------- Валидации ----------

    async def _validate_premise_ids(
        self, project_id: UUID, premise_ids: list[UUID],
    ) -> None:
        """Вводные должны существовать и принадлежать проекту."""
        for pid in premise_ids:
            premise = await self._premise_repo.get_by_id(pid)
            if premise is None:
                raise ValueError(f"Вводная {pid} не найдена для связи с решением")
            if UUID(str(premise.project_id)) != UUID(str(project_id)):
                raise ValueError(
                    f"Вводная {pid} принадлежит другому проекту"
                )

    async def _validate_goal_ids(
        self, project_id: UUID, goal_ids: list[UUID],
    ) -> None:
        """Цели должны существовать и принадлежать проекту."""
        for gid in goal_ids:
            goal = await self._goal_repo.get_by_id(gid)
            if goal is None:
                raise ValueError(f"Цель {gid} не найдена для связи с решением")
            if UUID(str(goal.project_id)) != UUID(str(project_id)):
                raise ValueError(
                    f"Цель {gid} принадлежит другому проекту"
                )
