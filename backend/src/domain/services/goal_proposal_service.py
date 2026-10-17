"""GoalProposalService — 4 правила вывода целей из вводных."""

import logging
from datetime import date, timedelta
from uuid import UUID

from backend.src.domain.entities.goal_proposal import GoalProposal
from backend.src.domain.entities.premise import Premise
from backend.src.domain.ports.repositories import PremiseRepository
from backend.src.domain.value_objects.enums import PremiseCategory

logger = logging.getLogger(__name__)


class GoalProposalService:
    """Сервис предложений целей на основе вводных.

    Прогоняет Premise проекта через 4 правила и агрегирует результаты.
    Не сохраняет в БД — возвращает эфемерный список предложений.
    """

    def __init__(self, premise_repo: PremiseRepository) -> None:
        self._premise_repo = premise_repo

    async def propose_goals(self, project_id: UUID) -> list[GoalProposal]:
        """Предложить цели для проекта на основе вводных.

        Загружает все Premise проекта, применяет 4 правила,
        дедуплицирует по formulation.

        Args:
            project_id: UUID проекта.

        Returns:
            Список предложений целей (не сохраняется в БД).
        """
        premises = await self._premise_repo.list_by_project(project_id)

        proposals: list[GoalProposal] = []
        proposals.extend(self._rule_contract(premises))
        proposals.extend(self._rule_tz(premises))
        proposals.extend(self._rule_customer_requirement(premises))
        proposals.extend(self._rule_source_data(premises))

        return self._deduplicate(proposals)

    # ---------- Правила ----------

    def _rule_contract(self, premises: list[Premise]) -> list[GoalProposal]:
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

    def _rule_tz(self, premises: list[Premise]) -> list[GoalProposal]:
        """Правило 2 — ТЗ → Goal.

        Если premise.category == TZ:
        - Если premise.data содержит requirement → использовать requirement.
        - Иначе → использовать name.
        """
        results: list[GoalProposal] = []
        for p in premises:
            if p.category != PremiseCategory.TZ:
                continue
            formulation = p.data.get("requirement") or p.name
            if not formulation:
                continue

            results.append(GoalProposal(
                formulation=formulation,
                rule="тз_требование",
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

    def _rule_source_data(self, premises: list[Premise]) -> list[GoalProposal]:
        """Правило 4 — просроченный ИД → Goal «Обновить ИД».

        Если premise.category == SOURCE_DATA и premise.valid_until < today,
        предложить цель "Обновить {name}" с дедлайном valid_until + 30 дней.
        """
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
    def _deduplicate(proposals: list[GoalProposal]) -> list[GoalProposal]:
        """Дедупликация по formulation.

        Если два правила дают одинаковую формулировку — объединить
        premise_ids, оставить первый rule.
        """
        seen: dict[str, GoalProposal] = {}
        for proposal in proposals:
            key = proposal.formulation.strip().lower()
            if key in seen:
                seen[key].premise_ids.extend(proposal.premise_ids)
            else:
                seen[key] = GoalProposal(
                    formulation=proposal.formulation,
                    rule=proposal.rule,
                    deadline=proposal.deadline,
                    priority=proposal.priority,
                    premise_ids=list(proposal.premise_ids),
                )
        return list(seen.values())
