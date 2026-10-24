"""RfiProposalService — правила вывода RFI (spec_week_4.md §6).

Система предлагает — ГИП утверждает (DOMAIN.md §2).
2 правила: decision_без_ид, rfi_просрочен.
"""

import logging
from datetime import date, timedelta
from uuid import NAMESPACE_DNS, UUID, uuid5

from backend.src.application.dto.rfi import RfiProposal
from backend.src.domain.entities.decision import Decision
from backend.src.domain.entities.task import Task
from backend.src.domain.ports.repositories import (
    DecisionRepository,
    RfiRepository,
)
from backend.src.domain.value_objects.enums import DecisionState, RfiState

logger = logging.getLogger(__name__)

DECISION_AGE_DAYS = 5
RFI_DUE_DATE_DELTA_DAYS = 14


class RfiProposalService:
    """Сервис предложений RFI.

    Прогоняет решения и RFI проекта через правила и агрегирует результаты.
    Не сохраняет в БД — возвращает эфемерный список предложений.
    Без дедупликации.
    """

    def __init__(
        self,
        decision_repo: DecisionRepository,
        rfi_repo: RfiRepository,
    ) -> None:
        self._decision_repo = decision_repo
        self._rfi_repo = rfi_repo

    async def propose_rfis(self, project_id: UUID) -> list[RfiProposal]:
        """Предложить RFI для проекта.

        Правила:
        1. decision_без_ид — Decision в state plan/in_progress,
           нет связанных Premise, created_at > N дней назад.
        2. rfi_просрочен — Task is_rfi=true, rfi_due_date < today,
           rfi_state NOT IN (closed, registered).

        Args:
            project_id: UUID проекта.

        Returns:
            Список предложений RFI (не сохраняется в БД).
        """
        decisions = await self._decision_repo.list_by_project(project_id)
        overdue_rfis = await self._rfi_repo.list_overdue(
            date.today(), project_id
        )

        logger.info(
            "Proposing rfis for project %s: %d decisions, %d overdue",
            project_id,
            len(decisions),
            len(overdue_rfis),
        )

        proposals: list[RfiProposal] = []
        for decision in decisions:
            proposals.extend(self._rule_decision_without_ids(decision))

        for task in overdue_rfis:
            proposals.extend(self._rule_rfi_overdue(task))

        # Детерминированные id для UI-ключей
        ns = uuid5(NAMESPACE_DNS, "gip-assistant-rfi-proposals")
        for p in proposals:
            if p.id is None:
                seed = f"{p.rule}:{p.formulation}:{p.existing_rfi_id}"
                p.id = uuid5(ns, seed)

        logger.info(
            "Proposed %d rfis for project %s",
            len(proposals),
            project_id,
        )
        return proposals

    # ---------- Правила ----------

    def _rule_decision_without_ids(
        self,
        decision: Decision,
    ) -> list[RfiProposal]:
        """Правило 1 — decision_без_ид.

        Decision в state plan/in_progress, нет связанных Premise,
        created_at > DECISION_AGE_DAYS дней назад.
        """
        if decision.state not in (DecisionState.PLAN, DecisionState.IN_PROGRESS):
            return []
        if decision.premise_ids:
            return []
        if decision.created_at is None:
            return []
        age = date.today() - decision.created_at.date()
        if age.days < DECISION_AGE_DAYS:
            return []

        return [
            RfiProposal(
                id=None,
                action="create",
                rule="decision_без_ид",
                formulation=f"Запросить ИД для решения: {decision.formulation}",
                rationale=None,
                reason_decision_id=decision.id,
                existing_rfi_id=None,
                rfi_due_date=date.today() + timedelta(days=RFI_DUE_DATE_DELTA_DAYS),
            )
        ]

    def _rule_rfi_overdue(self, task: Task) -> list[RfiProposal]:
        """Правило 2 — rfi_просрочен.

        Task is_rfi=true, rfi_due_date < today,
        rfi_state NOT IN (closed, registered).
        """
        if task.rfi_state is None:
            return []
        if task.rfi_due_date is None:
            return []
        if task.rfi_state in (RfiState.CLOSED, RfiState.REGISTERED):
            return []
        if task.rfi_due_date >= date.today():
            return []

        days_overdue = (date.today() - task.rfi_due_date).days

        return [
            RfiProposal(
                id=None,
                action="escalate",
                rule="rfi_просрочен",
                formulation=f"Эскалировать RFI: {task.title}",
                rationale=f"Просрочен на {days_overdue} дней",
                reason_decision_id=None,
                existing_rfi_id=task.id,
                rfi_due_date=None,
            )
        ]
