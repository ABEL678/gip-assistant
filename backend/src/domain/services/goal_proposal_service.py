"""GoalProposalService — правила вывода целей и стандартов из вводных."""

import logging
from datetime import date, timedelta
from typing import Any
from uuid import NAMESPACE_DNS, UUID, uuid5

from backend.src.domain.entities.goal_proposal import GoalProposal
from backend.src.domain.entities.premise import Premise
from backend.src.domain.ports.repositories import PremiseRepository
from backend.src.domain.value_objects.enums import PremiseCategory, ProjectStandardType

logger = logging.getLogger(__name__)


class GoalProposalService:
    """Сервис предложений целей и стандартов на основе вводных.

    Прогоняет Premise проекта через правила и агрегирует результаты.
    Не сохраняет в БД — возвращает эфемерные списки предложений.
    """

    def __init__(self, premise_repo: PremiseRepository) -> None:
        self._premise_repo = premise_repo

    async def propose_goals(self, project_id: UUID) -> list[GoalProposal]:
        """Предложить цели для проекта на основе вводных.

        Загружает все Premise проекта, применяет правила 1, 3, 4,
        дедуплицирует по formulation.

        Args:
            project_id: UUID проекта.

        Returns:
            Список предложений целей (не сохраняется в БД).
        """
        premises = await self._premise_repo.list_by_project(project_id)
        logger.info(
            "Proposing goals for project %s: %d premises",
            project_id,
            len(premises),
        )
        for p in premises:
            logger.info(
                "  Premise: cat=%s name=%r data=%s",
                p.category,
                p.name,
                p.data,
            )

        proposals: list[GoalProposal] = []
        proposals.extend(self._rule_contract(premises))
        proposals.extend(self._rule_customer_requirement(premises))
        proposals.extend(self._rule_source_data(premises))

        logger.info("Proposals before dedup: %d", len(proposals))
        result = self._deduplicate(proposals)
        # Генерируем id для каждого предложения (нужен для React key)
        for p in result:
            if p.id is None:
                ns = uuid5(NAMESPACE_DNS, "gip-assistant-proposals")
                seed = f"{p.rule}:{p.formulation}"
                p.id = uuid5(ns, seed)
        logger.info("Proposals after dedup: %d", len(result))
        for r in result:
            logger.info(
                "  Proposal: id=%s rule=%s formulation=%r",
                r.id, r.rule, r.formulation,
            )

        return result

    async def propose_standards(
        self, project_id: UUID,
    ) -> list[dict[str, Any]]:
        """Предложить стандарты (правило 2: ТЗ → ProjectStandard).

        Если premise.category == TZ и premise.data содержит requirement,
        предложить ProjectStandard с type=COMPOSITION.

        Args:
            project_id: UUID проекта.

        Returns:
            Список словарей стандартов для создания.
        """
        premises = await self._premise_repo.list_by_project(project_id)
        standards: list[dict[str, Any]] = []
        for p in premises:
            if p.category != PremiseCategory.TZ:
                continue
            requirement = p.data.get("requirement")
            if requirement:
                standards.append({
                    "premise_id": p.id,
                    "type": ProjectStandardType.COMPOSITION,
                    "value": {"requirement": requirement},
                })
        return standards

    # ---------- Правила ----------

    def _rule_contract(
        self, premises: list[Premise],
    ) -> list[GoalProposal]:
        """Правило 1 — договор со сроком → Goal.

        Если premise.category == CONTRACT и premise.data содержит deadline,
        предложить цель "Сдать {name} к {deadline}".
        """
        results: list[GoalProposal] = []
        for p in premises:
            if p.category != PremiseCategory.CONTRACT:
                continue
            deadline_str = p.data.get("deadline")
            if not deadline_str:
                continue

            deadline = self._parse_date(deadline_str)
            if deadline is None:
                continue

            results.append(GoalProposal(
                formulation=f"Сдать {p.name} к {deadline}",
                rule="договор_срок",
                deadline=deadline,
                premise_ids=[p.id],
            ))
        return results

    def _rule_customer_requirement(
        self, premises: list[Premise],
    ) -> list[GoalProposal]:
        """Правило 3 — требование Заказчика → Goal.

        Если premise.category == CUSTOMER_REQUIREMENT и premise.data
        содержит content, предложить цель с формулировкой из content.
        """
        results: list[GoalProposal] = []
        for p in premises:
            if p.category != PremiseCategory.CUSTOMER_REQUIREMENT:
                continue
            content = p.data.get("content")
            if not content:
                continue

            results.append(GoalProposal(
                formulation=content,
                rule="требование_заказчика",
                premise_ids=[p.id],
            ))
        return results

    def _rule_source_data(
        self, premises: list[Premise],
    ) -> list[GoalProposal]:
        """Правило 4 — просроченный ИД → Goal «Обновить ИД»."""
        today = date.today()
        results: list[GoalProposal] = []
        for p in premises:
            if p.category != PremiseCategory.SOURCE_DATA:
                continue
            if p.valid_until is None or p.valid_until >= today:
                continue

            deadline = p.valid_until + timedelta(days=30)
            results.append(GoalProposal(
                formulation=f"Обновить {p.name}",
                rule="просроченный_ид",
                deadline=deadline,
                premise_ids=[p.id],
            ))
        return results

    # ---------- Утилиты ----------

    @staticmethod
    def _parse_date(value) -> date | None:
        """Парсить дату из строки или вернуть как есть."""
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            try:
                return date.fromisoformat(value)
            except (ValueError, TypeError):
                return None
        return None

    @staticmethod
    def _deduplicate(
        proposals: list[GoalProposal],
    ) -> list[GoalProposal]:
        """Дедупликация по formulation."""
        seen: dict[str, GoalProposal] = {}
        for proposal in proposals:
            key = proposal.formulation.strip().lower()
            if key in seen:
                seen[key].premise_ids.extend(proposal.premise_ids)
                seen[key].confidence = min(
                    seen[key].confidence, proposal.confidence,
                )
            else:
                seen[key] = GoalProposal(
                    formulation=proposal.formulation,
                    rule=proposal.rule,
                    deadline=proposal.deadline,
                    priority=proposal.priority,
                    premise_ids=list(proposal.premise_ids),
                    confidence=proposal.confidence,
                )
        return list(seen.values())
