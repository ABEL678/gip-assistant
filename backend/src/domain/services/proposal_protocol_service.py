"""Протокол 2–3 прогонов (spec_week_1.md §6.3.1)."""

from collections import Counter
from uuid import UUID

from backend.src.application.dto.protocol_summary import ProtocolSummary
from backend.src.domain.ports.goal_validator import GoalValidatorService
from backend.src.domain.ports.repositories import GoalRepository


class ProposalProtocolService:
    """Свод протокола 2–3 прогонов."""

    def __init__(self, goal_repo: GoalRepository) -> None:
        self._goal_repo = goal_repo

    async def run(
        self,
        project_id: UUID,
        validators: list[GoalValidatorService],
    ) -> ProtocolSummary:
        """Прогнать всех валидаторов на каждом Goal, свести результаты."""
        if not validators:
            raise ValueError("validators must not be empty")

        goals = await self._goal_repo.list_by_project(project_id)

        if not goals:
            return ProtocolSummary(total=0)

        unanimous: dict[UUID, object] = {}
        majority: dict[UUID, object] = {}
        split: list[UUID] = []

        for goal in goals:
            statuses = [
                await v.validate(goal.id) for v in validators
            ]
            status_list = [s.verification_status for s in statuses]
            counter = Counter(status_list)
            most_common_count = counter.most_common(1)[0][1]
            dominant_status = counter.most_common(1)[0][0]

            if most_common_count == len(validators):
                unanimous[goal.id] = dominant_status
            elif most_common_count * 2 > len(validators):
                majority[goal.id] = dominant_status
            else:
                split.append(goal.id)

        return ProtocolSummary(
            total=len(goals),
            unanimous=dict(unanimous),
            majority=dict(majority),
            split=split,
        )
