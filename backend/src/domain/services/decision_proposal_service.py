"""DecisionProposalService — правила вывода решений из целей (spec_week_3 §6).

Система предлагает — ГИП утверждает (DOMAIN.md §2).
Правила (вехи 1–5): только явное, выводимое из вводных.
"""

import logging
from uuid import NAMESPACE_DNS, UUID, uuid5

from backend.src.domain.entities.decision_proposal import DecisionProposal
from backend.src.domain.entities.goal import Goal
from backend.src.domain.ports.repositories import (
    DecisionRepository,
    GoalRepository,
)
from backend.src.domain.value_objects.enums import DecisionState

logger = logging.getLogger(__name__)


class DecisionProposalService:
    """Сервис предложений решений на основе целей.

    Прогоняет Goal проекта через правила и агрегирует результаты.
    Не сохраняет в БД — возвращает эфемерный список предложений.
    Без дедупликации: один Goal может дать два предложения
    (по одному от каждого правила).
    """

    def __init__(
        self,
        goal_repo: GoalRepository,
        decision_repo: DecisionRepository,
    ) -> None:
        self._goal_repo = goal_repo
        self._decision_repo = decision_repo

    async def propose_decisions(
        self, project_id: UUID,
    ) -> list[DecisionProposal]:
        """Предложить решения для проекта.

        Правила:
        1. goal_без_решения — у Goal нет связанных Decision.
        2. срок_из_вводных — у Goal есть deadline и premise_ids.

        Args:
            project_id: UUID проекта.

        Returns:
            Список предложений решений (не сохраняется в БД).
        """
        goals = await self._goal_repo.list_by_project(project_id)
        decisions = await self._decision_repo.list_by_project(project_id)
        logger.info(
            "Proposing decisions for project %s: %d goals, %d decisions",
            project_id,
            len(goals),
            len(decisions),
        )

        # Цели, у которых уже есть решения (по decision_goals)
        covered_goal_ids = {
            gid for decision in decisions for gid in decision.goal_ids
        }

        proposals: list[DecisionProposal] = []
        for goal in goals:
            proposals.extend(self._rule_goal_without_decision(goal, covered_goal_ids))
            proposals.extend(self._rule_deadline_from_premises(goal))

        # Детерминированные id для UI-ключей (паттерн GoalProposalService)
        ns = uuid5(NAMESPACE_DNS, "gip-assistant-proposals")
        for p in proposals:
            if p.id is None:
                seed = f"{p.rule}:{p.formulation}:{p.goal_ids}"
                p.id = uuid5(ns, seed)

        logger.info("Proposed %d decisions for project %s", len(proposals), project_id)
        return proposals

    # ---------- Правила ----------

    def _rule_goal_without_decision(
        self, goal: Goal, covered_goal_ids: set[UUID],
    ) -> list[DecisionProposal]:
        """Правило 1 — Goal без Decision → «Определить способ реализации»."""
        if goal.id in covered_goal_ids:
            return []
        return [DecisionProposal(
            formulation=f"Определить способ реализации цели: {goal.formulation}",
            rule="goal_без_решения",
            state=DecisionState.PLAN,
            goal_ids=[goal.id],
        )]

    def _rule_deadline_from_premises(self, goal: Goal) -> list[DecisionProposal]:
        """Правило 2 — Goal с deadline и premise_ids → «Обосновать срок»."""
        if goal.deadline is None or not goal.premise_ids:
            return []
        return [DecisionProposal(
            formulation=f"Обосновать срок: {goal.formulation}",
            rule="срок_из_вводных",
            rationale=f"Срок {goal.deadline} из вводных",
            state=DecisionState.PLAN,
            premise_ids=list(goal.premise_ids),
            goal_ids=[goal.id],
        )]
