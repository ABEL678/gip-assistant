"""Агент-валидатор Goal (spec_week_1.md §6.1.1).

Работает на правилах (веха 1–5), без LLM.
Проверяет Goal на доказанность: два места в вводных, owner у каждой цифры,
отсутствие противоречий.
"""

import re
from datetime import date as _date
from uuid import UUID

from backend.src.application.dto.validation_result import (
    ValidationEvidence,
    ValidationResult,
)
from backend.src.domain.ports.repositories import (
    GoalRepository,
    PremiseRepository,
)
from backend.src.domain.value_objects.enums import VerificationStatus


def _parse_date(value: object) -> object:
    """Парсит дату из строки или возвращает как есть."""
    if isinstance(value, str):
        return _date.fromisoformat(value)
    return value


class GoalValidatorService:
    """Проверяет Goal на доказанность (правила 1–6 спеки §6.1.1)."""

    def __init__(
        self,
        goal_repo: GoalRepository,
        premise_repo: PremiseRepository,
    ) -> None:
        self._goal_repo = goal_repo
        self._premise_repo = premise_repo

    async def validate(self, goal_id: UUID) -> ValidationResult:
        """Прогнать правила 1–6, обновить goal.verification_status, вернуть результат."""
        goal = await self._goal_repo.get_by_id(goal_id)
        if goal is None:
            raise ValueError(f"Goal {goal_id} not found")

        missing: list[str] = []
        contradictions: list[str] = []
        evidence: list[ValidationEvidence] = []

        # Флаги типов провалов (для Rule 6)
        has_no_data: bool = False
        has_contradiction: bool = False
        has_requires_check: bool = False

        # Rule 1: нет premise_ids → NO_DATA
        if not goal.premise_ids:
            has_no_data = True
            missing.append("no premise_ids")
        else:
            # Загрузить premises
            premises = [
                p
                for pid in goal.premise_ids
                if (p := await self._premise_repo.get_by_id(pid)) is not None
            ]

            # Rule 2: проверить owner у каждого поля data → NO_DATA
            for premise in premises:
                for field_name in premise.data:
                    field_obj = premise.data_field(field_name)
                    if field_obj is None or field_obj.owner is None:
                        missing.append(f"{premise.name}.{field_name}: no owner")
                        has_no_data = True

            # Rule 3: посчитать источники → REQUIRES_CHECK
            source_premises = [
                p
                for p in premises
                if any(
                    pf.owner is not None
                    for pf in (p.data_field(fn) for fn in p.data)
                    if pf is not None
                )
            ]
            if len(source_premises) < 2:
                has_requires_check = True
                missing.append("<2 sources")

            # Собрать evidence из источников
            for premise in premises:
                for field_name in premise.data:
                    field_obj = premise.data_field(field_name)
                    if field_obj is not None and field_obj.owner is not None:
                        evidence.append(
                            ValidationEvidence(
                                premise_id=premise.id,
                                field=field_name,
                                value=field_obj.value,
                                owner=field_obj.owner,
                            )
                        )

            # Rule 4: проверить источник для deadline → NO_DATA
            if goal.deadline is not None:
                deadline_found = False
                for premise in premises:
                    df = premise.data_field("deadline")
                    if df is not None and df.owner is not None:
                        try:
                            pd = _parse_date(df.value)
                            if pd == goal.deadline:
                                deadline_found = True
                                break
                        except (ValueError, TypeError):
                            continue
                if not deadline_found:
                    has_no_data = True
                    missing.append("no source for deadline")

            # Числа в formulation — мягкое предупреждение (не меняет статус)
            numbers = re.findall(r"\d+", goal.formulation)
            if numbers:
                for num_str in numbers:
                    found = False
                    for premise in premises:
                        for field_name in premise.data:
                            field_obj = premise.data_field(field_name)
                            if field_obj is not None and field_obj.owner is not None:
                                if str(field_obj.value) == num_str:
                                    found = True
                                    break
                        if found:
                            break
                    if not found:
                        missing.append(f"no source for {num_str}")

            # Rule 5: противоречие deadline с договором → NOT_CONFIRMED
            if goal.deadline is not None:
                for premise in premises:
                    if premise.category.value == "contract":
                        df = premise.data_field("deadline")
                        if df is not None and df.owner is not None:
                            try:
                                pd = _parse_date(df.value)
                                if goal.deadline > pd:
                                    has_contradiction = True
                                    contradictions.append(
                                        "deadline later than contract"
                                    )
                            except (ValueError, TypeError):
                                pass

        # Rule 6: итоговый статус
        # Приоритет: NOT_CONFIRMED > NO_DATA > REQUIRES_CHECK
        if has_contradiction:
            status = VerificationStatus.NOT_CONFIRMED
        elif has_no_data:
            status = VerificationStatus.NO_DATA
        elif has_requires_check:
            status = VerificationStatus.REQUIRES_CHECK
        else:
            status = VerificationStatus.CONFIRMED

        goal.verification_status = status
        await self._goal_repo.save(goal)

        return ValidationResult(
            goal_id=goal.id,
            verification_status=status,
            evidence=evidence,
            missing=missing,
            contradictions=contradictions,
        )
