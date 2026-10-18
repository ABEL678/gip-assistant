"""Тесты ProposalProtocolService."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from backend.src.application.dto.protocol_summary import ProtocolSummary
from backend.src.application.dto.validation_result import ValidationResult
from backend.src.domain.entities.goal import Goal
from backend.src.domain.ports.goal_validator import GoalValidatorService
from backend.src.domain.services.proposal_protocol_service import (
    ProposalProtocolService,
)
from backend.src.domain.value_objects.enums import VerificationStatus


class _MockValidator(GoalValidatorService):
    """Мок-валидатор, возвращающий заданный статус."""

    def __init__(self, status: VerificationStatus) -> None:
        self._status = status

    async def validate(self, goal_id) -> ValidationResult:
        return ValidationResult(
            goal_id=goal_id,
            verification_status=self._status,
        )


def _make_goal() -> Goal:
    return Goal(
        id=uuid4(),
        project_id=uuid4(),
        formulation="Test goal",
    )


@pytest.fixture
def goal_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.list_by_project = AsyncMock()
    return repo


@pytest.fixture
def service(goal_repo: AsyncMock) -> ProposalProtocolService:
    return ProposalProtocolService(goal_repo)


# --- Tests ---


@pytest.mark.asyncio
async def test_empty_goals(service: ProposalProtocolService, goal_repo: AsyncMock):
    """Нет goal → ProtocolSummary(total=0), все поля пустые."""
    goal_repo.list_by_project.return_value = []

    result = await service.run(uuid4(), [_MockValidator(VerificationStatus.CONFIRMED)])

    assert result.total == 0
    assert result.unanimous == {}
    assert result.majority == {}
    assert result.split == []


@pytest.mark.asyncio
async def test_unanimous(service: ProposalProtocolService, goal_repo: AsyncMock):
    """2 Goal, 3 mock все CONFIRMED → unanimous содержит оба."""
    goal1 = _make_goal()
    goal2 = _make_goal()
    goal_repo.list_by_project.return_value = [goal1, goal2]

    validators = [
        _MockValidator(VerificationStatus.CONFIRMED),
        _MockValidator(VerificationStatus.CONFIRMED),
        _MockValidator(VerificationStatus.CONFIRMED),
    ]

    result = await service.run(uuid4(), validators)

    assert result.total == 2
    assert goal1.id in result.unanimous
    assert goal2.id in result.unanimous
    assert result.unanimous[goal1.id] == VerificationStatus.CONFIRMED
    assert result.unanimous[goal2.id] == VerificationStatus.CONFIRMED
    assert result.majority == {}
    assert result.split == []


@pytest.mark.asyncio
async def test_majority(service: ProposalProtocolService, goal_repo: AsyncMock):
    """1 Goal, 2 mock CONFIRMED + 1 mock NO_DATA → majority[goal.id] = CONFIRMED."""
    goal = _make_goal()
    goal_repo.list_by_project.return_value = [goal]

    validators = [
        _MockValidator(VerificationStatus.CONFIRMED),
        _MockValidator(VerificationStatus.CONFIRMED),
        _MockValidator(VerificationStatus.NO_DATA),
    ]

    result = await service.run(uuid4(), validators)

    assert result.total == 1
    assert goal.id in result.majority
    assert result.majority[goal.id] == VerificationStatus.CONFIRMED
    assert goal.id not in result.unanimous


@pytest.mark.asyncio
async def test_split(service: ProposalProtocolService, goal_repo: AsyncMock):
    """1 Goal, 3 mock с разными статусами → split = [goal.id]."""
    goal = _make_goal()
    goal_repo.list_by_project.return_value = [goal]

    validators = [
        _MockValidator(VerificationStatus.CONFIRMED),
        _MockValidator(VerificationStatus.NO_DATA),
        _MockValidator(VerificationStatus.REQUIRES_CHECK),
    ]

    result = await service.run(uuid4(), validators)

    assert result.total == 1
    assert result.split == [goal.id]
    assert goal.id not in result.unanimous
    assert goal.id not in result.majority


@pytest.mark.asyncio
async def test_multiple_goals_mixed(
    service: ProposalProtocolService, goal_repo: AsyncMock
):
    """2 Goal: один unanimous, другой split → корректный свод."""
    goal1 = _make_goal()
    goal2 = _make_goal()
    goal_repo.list_by_project.return_value = [goal1, goal2]

    # goal1: unanimous CONFIRMED (все 3 валидатора возвращают CONFIRMED)
    # goal2: split (разные статусы от разных валидаторов)
    class MixedValidator(GoalValidatorService):
        def __init__(self, goal2_status: VerificationStatus) -> None:
            self._goal2_status = goal2_status

        async def validate(self, goal_id):
            if goal_id == goal2.id:
                return ValidationResult(
                    goal_id=goal_id,
                    verification_status=self._goal2_status,
                )
            return ValidationResult(
                goal_id=goal_id,
                verification_status=VerificationStatus.CONFIRMED,
            )

    validators = [
        MixedValidator(VerificationStatus.CONFIRMED),
        MixedValidator(VerificationStatus.NO_DATA),
        MixedValidator(VerificationStatus.REQUIRES_CHECK),
    ]

    result = await service.run(uuid4(), validators)

    assert result.total == 2
    assert goal1.id in result.unanimous
    assert result.unanimous[goal1.id] == VerificationStatus.CONFIRMED
    assert goal2.id in result.split


@pytest.mark.asyncio
async def test_one_validator(service: ProposalProtocolService, goal_repo: AsyncMock):
    """1 Goal, 1 mock CONFIRMED → unanimous[goal.id] = CONFIRMED."""
    goal = _make_goal()
    goal_repo.list_by_project.return_value = [goal]

    validators = [_MockValidator(VerificationStatus.CONFIRMED)]

    result = await service.run(uuid4(), validators)

    assert result.total == 1
    assert goal.id in result.unanimous
    assert result.unanimous[goal.id] == VerificationStatus.CONFIRMED


@pytest.mark.asyncio
async def test_dominant_status_in_majority(
    service: ProposalProtocolService, goal_repo: AsyncMock
):
    """1 Goal, 2 mock NO_DATA + 1 mock CONFIRMED → majority[goal.id] = NO_DATA."""
    goal = _make_goal()
    goal_repo.list_by_project.return_value = [goal]

    validators = [
        _MockValidator(VerificationStatus.NO_DATA),
        _MockValidator(VerificationStatus.NO_DATA),
        _MockValidator(VerificationStatus.CONFIRMED),
    ]

    result = await service.run(uuid4(), validators)

    assert result.total == 1
    assert goal.id in result.majority
    assert result.majority[goal.id] == VerificationStatus.NO_DATA
