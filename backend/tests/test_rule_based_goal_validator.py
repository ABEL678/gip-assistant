"""Тесты RuleBasedGoalValidator."""

from datetime import date
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from backend.src.application.dto.validation_result import (
    ValidationEvidence,
    ValidationResult,
)
from backend.src.domain.entities.goal import Goal
from backend.src.domain.entities.premise import Premise
from backend.src.domain.entities.project_standard import ProjectStandard
from backend.src.domain.entities.result import Result
from backend.src.domain.services.rule_based_goal_validator import (
    RuleBasedGoalValidator,
)
from backend.src.domain.value_objects.enums import (
    GoalState,
    PremiseCategory,
    ProjectStandardType,
    VerificationStatus,
)


@pytest.fixture
def mock_goal_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.list_by_project = AsyncMock()
    repo.save = AsyncMock()
    repo.delete = AsyncMock()
    return repo


@pytest.fixture
def mock_premise_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.list_by_project = AsyncMock()
    repo.list_by_source_goal = AsyncMock()
    return repo


@pytest.fixture
def mock_result_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.list_by_project = AsyncMock()
    repo.list_by_goal = AsyncMock()
    return repo


@pytest.fixture
def mock_standard_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.list_by_premise = AsyncMock()
    repo.list_by_type = AsyncMock()
    repo.list_by_goal = AsyncMock()
    return repo


@pytest.fixture
def service(
    mock_goal_repo: AsyncMock,
    mock_premise_repo: AsyncMock,
    mock_result_repo: AsyncMock,
    mock_standard_repo: AsyncMock,
) -> RuleBasedGoalValidator:
    return RuleBasedGoalValidator(
        goal_repo=mock_goal_repo,
        premise_repo=mock_premise_repo,
        result_repo=mock_result_repo,
        standard_repo=mock_standard_repo,
    )


# --- Helpers ---


def _make_premise(
    category: PremiseCategory = PremiseCategory.CONTRACT,
    data: dict | None = None,
    name: str = "Test Premise",
) -> Premise:
    return Premise(
        id=uuid4(),
        project_id=uuid4(),
        category=category,
        name=name,
        data=data or {},
    )


def _make_goal(
    premise_ids: list | None = None,
    deadline: date | None = None,
    formulation: str = "Сдать проект",
) -> Goal:
    return Goal(
        id=uuid4(),
        project_id=uuid4(),
        formulation=formulation,
        deadline=deadline,
        premise_ids=premise_ids or [],
    )


# --- Tests ---


@pytest.mark.asyncio
async def test_validate_no_premise_ids(
    service: RuleBasedGoalValidator,
    mock_goal_repo: AsyncMock,
):
    """Rule 1: пустые premise_ids → NO_DATA."""
    goal = _make_goal(premise_ids=[])
    mock_goal_repo.get_by_id.return_value = goal

    result = await service.validate(goal.id)

    assert result.verification_status == VerificationStatus.NO_DATA
    assert result.missing == ["no premise_ids"]
    assert result.evidence == []
    mock_goal_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_validate_premise_without_owner(
    service: RuleBasedGoalValidator,
    mock_goal_repo: AsyncMock,
    mock_premise_repo: AsyncMock,
):
    """Rule 2: premise без owner → NO_DATA."""
    premise = _make_premise(
        data={
            "deadline": {"value": "2026-12-01", "owner": None, "source": None},
        }
    )
    goal = _make_goal(premise_ids=[premise.id])
    mock_goal_repo.get_by_id.return_value = goal
    mock_premise_repo.get_by_id.return_value = premise

    result = await service.validate(goal.id)

    assert result.verification_status == VerificationStatus.NO_DATA
    assert any("no owner" in m for m in result.missing)


@pytest.mark.asyncio
async def test_validate_less_than_two_sources(
    service: RuleBasedGoalValidator,
    mock_goal_repo: AsyncMock,
    mock_premise_repo: AsyncMock,
):
    """Rule 3: меньше двух источников → REQUIRES_CHECK."""
    premise = _make_premise(
        data={
            "deadline": {"value": "2026-12-01", "owner": "contract", "source": None},
        }
    )
    goal = _make_goal(premise_ids=[premise.id])
    mock_goal_repo.get_by_id.return_value = goal
    mock_premise_repo.get_by_id.return_value = premise

    result = await service.validate(goal.id)

    assert result.verification_status == VerificationStatus.REQUIRES_CHECK
    assert any("<2 sources" in m for m in result.missing)


@pytest.mark.asyncio
async def test_validate_confirmed_happy_path(
    service: RuleBasedGoalValidator,
    mock_goal_repo: AsyncMock,
    mock_premise_repo: AsyncMock,
):
    """Rule 4-6: два premise с owner, deadline совпадает → CONFIRMED."""
    deadline = date(2026, 12, 1)
    premise1 = _make_premise(
        category=PremiseCategory.CONTRACT,
        data={
            "deadline": {"value": "2026-12-01", "owner": "contract", "source": None},
        },
        name="Договор",
    )
    premise2 = _make_premise(
        category=PremiseCategory.TZ,
        data={
            "requirement": {
                "value": "Сдать том 7",
                "owner": "tz",
                "source": None,
            },
        },
        name="ТЗ",
    )
    goal = _make_goal(
        premise_ids=[premise1.id, premise2.id],
        deadline=deadline,
        formulation="Сдать проект",
    )
    mock_goal_repo.get_by_id.return_value = goal
    mock_premise_repo.get_by_id.side_effect = [premise1, premise2]

    result = await service.validate(goal.id)

    assert result.verification_status == VerificationStatus.CONFIRMED
    assert result.missing == []
    assert result.contradictions == []
    assert len(result.evidence) == 2
    mock_goal_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_validate_deadline_later_than_contract(
    service: RuleBasedGoalValidator,
    mock_goal_repo: AsyncMock,
    mock_premise_repo: AsyncMock,
):
    """Rule 5: goal.deadline > contract.deadline → NOT_CONFIRMED."""
    contract_deadline = date(2026, 6, 1)
    goal_deadline = date(2026, 12, 1)
    premise = _make_premise(
        category=PremiseCategory.CONTRACT,
        data={
            "deadline": {
                "value": "2026-06-01",
                "owner": "contract",
                "source": None,
            },
        },
        name="Договор",
    )
    goal = _make_goal(
        premise_ids=[premise.id],
        deadline=goal_deadline,
    )
    mock_goal_repo.get_by_id.return_value = goal
    mock_premise_repo.get_by_id.return_value = premise

    result = await service.validate(goal.id)

    assert result.verification_status == VerificationStatus.NOT_CONFIRMED
    assert any(
        "deadline later than contract" in c for c in result.contradictions
    )
    # При противоречии — нет ложного "no source for deadline" в missing
    assert "no source for deadline" not in result.missing


@pytest.mark.asyncio
async def test_validate_deadline_later_than_contract_no_missing_no_source(
    service: RuleBasedGoalValidator,
    mock_goal_repo: AsyncMock,
    mock_premise_repo: AsyncMock,
):
    """Rule 4+5: goal.deadline > contract.deadline — нет ложного no_data в missing."""
    goal_deadline = date(2026, 12, 1)
    premise = _make_premise(
        category=PremiseCategory.CONTRACT,
        data={
            "deadline": {
                "value": "2026-06-01",
                "owner": "contract",
                "source": None,
            },
        },
        name="Договор",
    )
    goal = _make_goal(
        premise_ids=[premise.id],
        deadline=goal_deadline,
    )
    mock_goal_repo.get_by_id.return_value = goal
    mock_premise_repo.get_by_id.return_value = premise

    result = await service.validate(goal.id)

    assert result.verification_status == VerificationStatus.NOT_CONFIRMED
    assert any(
        "deadline later than contract" in c for c in result.contradictions
    )
    assert "no source for deadline" not in result.missing


@pytest.mark.asyncio
async def test_validate_no_source_for_deadline(
    service: RuleBasedGoalValidator,
    mock_goal_repo: AsyncMock,
    mock_premise_repo: AsyncMock,
):
    """Rule 4: goal.deadline есть, но нет premise с deadline data → NO_DATA."""
    deadline = date(2026, 12, 1)
    premise = _make_premise(
        category=PremiseCategory.TZ,
        data={
            "requirement": {
                "value": "Сдать том 7",
                "owner": "tz",
                "source": None,
            },
        },
        name="ТЗ",
    )
    goal = _make_goal(
        premise_ids=[premise.id],
        deadline=deadline,
    )
    mock_goal_repo.get_by_id.return_value = goal
    mock_premise_repo.get_by_id.return_value = premise

    result = await service.validate(goal.id)

    assert result.verification_status == VerificationStatus.NO_DATA
    assert any("no source for deadline" in m for m in result.missing)


@pytest.mark.asyncio
async def test_validate_goal_not_found(
    service: RuleBasedGoalValidator,
    mock_goal_repo: AsyncMock,
):
    """Goal не найден → ValueError."""
    mock_goal_repo.get_by_id.return_value = None
    target_id = uuid4()

    with pytest.raises(ValueError, match="not found"):
        await service.validate(target_id)

    mock_goal_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_validate_saves_status(
    service: RuleBasedGoalValidator,
    mock_goal_repo: AsyncMock,
    mock_premise_repo: AsyncMock,
):
    """save вызван с обновлённым verification_status."""
    deadline = date(2026, 12, 1)
    premise1 = _make_premise(
        category=PremiseCategory.CONTRACT,
        data={
            "deadline": {"value": "2026-12-01", "owner": "contract", "source": None},
        },
        name="Договор",
    )
    premise2 = _make_premise(
        category=PremiseCategory.TZ,
        data={
            "requirement": {
                "value": "Сдать том 7",
                "owner": "tz",
                "source": None,
            },
        },
        name="ТЗ",
    )
    goal = _make_goal(
        premise_ids=[premise1.id, premise2.id],
        deadline=deadline,
    )
    # Начальный статус — REQUIRES_CHECK
    assert goal.verification_status == VerificationStatus.REQUIRES_CHECK
    mock_goal_repo.get_by_id.return_value = goal
    mock_premise_repo.get_by_id.side_effect = [premise1, premise2]

    await service.validate(goal.id)

    # Проверить что save был вызван
    mock_goal_repo.save.assert_called_once()
    saved_goal = mock_goal_repo.save.call_args[0][0]
    assert saved_goal.verification_status == VerificationStatus.CONFIRMED


# --- Steps 7–9 ---


@pytest.mark.asyncio
async def test_validate_no_project_standard(
    service: RuleBasedGoalValidator,
    mock_goal_repo: AsyncMock,
    mock_premise_repo: AsyncMock,
    mock_standard_repo: AsyncMock,
):
    """Step 7: нет ProjectStandard → REQUIRES_CHECK."""
    deadline = date(2026, 12, 1)
    premise1 = _make_premise(
        category=PremiseCategory.CONTRACT,
        data={
            "deadline": {"value": "2026-12-01", "owner": "contract", "source": None},
        },
        name="Договор",
    )
    premise2 = _make_premise(
        category=PremiseCategory.TZ,
        data={
            "requirement": {
                "value": "Сдать том 7",
                "owner": "tz",
                "source": None,
            },
        },
        name="ТЗ",
    )
    goal = _make_goal(
        premise_ids=[premise1.id, premise2.id],
        deadline=deadline,
    )
    mock_goal_repo.get_by_id.return_value = goal
    mock_premise_repo.get_by_id.side_effect = [premise1, premise2]
    mock_standard_repo.list_by_goal.return_value = []

    result = await service.validate(goal.id)

    assert result.verification_status == VerificationStatus.REQUIRES_CHECK
    assert any("no ProjectStandard" in m for m in result.missing)


@pytest.mark.asyncio
async def test_validate_no_result(
    service: RuleBasedGoalValidator,
    mock_goal_repo: AsyncMock,
    mock_premise_repo: AsyncMock,
    mock_standard_repo: AsyncMock,
    mock_result_repo: AsyncMock,
):
    """Step 8: нет Result → REQUIRES_CHECK."""
    deadline = date(2026, 12, 1)
    premise1 = _make_premise(
        category=PremiseCategory.CONTRACT,
        data={
            "deadline": {"value": "2026-12-01", "owner": "contract", "source": None},
        },
        name="Договор",
    )
    premise2 = _make_premise(
        category=PremiseCategory.TZ,
        data={
            "requirement": {
                "value": "Сдать том 7",
                "owner": "tz",
                "source": None,
            },
        },
        name="ТЗ",
    )
    goal = _make_goal(
        premise_ids=[premise1.id, premise2.id],
        deadline=deadline,
    )
    mock_goal_repo.get_by_id.return_value = goal
    mock_premise_repo.get_by_id.side_effect = [premise1, premise2]

    std = ProjectStandard(
        id=uuid4(),
        premise_id=uuid4(),
        type=ProjectStandardType.DEADLINE,
        value={"deadline": "2026-12-01"},
    )
    mock_standard_repo.list_by_goal.return_value = [std]
    mock_result_repo.list_by_goal.return_value = []

    result = await service.validate(goal.id)

    assert result.verification_status == VerificationStatus.REQUIRES_CHECK
    assert any("no Result" in m for m in result.missing)


@pytest.mark.asyncio
async def test_validate_achieved_goal_no_premise(
    service: RuleBasedGoalValidator,
    mock_goal_repo: AsyncMock,
    mock_premise_repo: AsyncMock,
    mock_standard_repo: AsyncMock,
    mock_result_repo: AsyncMock,
):
    """Step 9: goal achieved но нет Premise (source_goal_id) → REQUIRES_CHECK."""
    deadline = date(2026, 12, 1)
    premise1 = _make_premise(
        category=PremiseCategory.CONTRACT,
        data={
            "deadline": {"value": "2026-12-01", "owner": "contract", "source": None},
        },
        name="Договор",
    )
    premise2 = _make_premise(
        category=PremiseCategory.TZ,
        data={
            "requirement": {
                "value": "Сдать том 7",
                "owner": "tz",
                "source": None,
            },
        },
        name="ТЗ",
    )
    goal = _make_goal(
        premise_ids=[premise1.id, premise2.id],
        deadline=deadline,
    )
    goal.state = GoalState.ACHIEVED
    mock_goal_repo.get_by_id.return_value = goal
    mock_premise_repo.get_by_id.side_effect = [premise1, premise2]

    std = ProjectStandard(
        id=uuid4(),
        premise_id=uuid4(),
        type=ProjectStandardType.DEADLINE,
        value={"deadline": "2026-12-01"},
    )
    mock_standard_repo.list_by_goal.return_value = [std]
    mock_result_repo.list_by_goal.return_value = [
        Result(id=uuid4(), project_id=uuid4(), formulation="Result")
    ]
    mock_premise_repo.list_by_source_goal.return_value = []

    result = await service.validate(goal.id)

    assert result.verification_status == VerificationStatus.REQUIRES_CHECK
    assert any(
        "goal achieved but no Premise" in m for m in result.missing
    )


@pytest.mark.asyncio
async def test_validate_standard_deadline_mismatch(
    service: RuleBasedGoalValidator,
    mock_goal_repo: AsyncMock,
    mock_premise_repo: AsyncMock,
    mock_standard_repo: AsyncMock,
    mock_result_repo: AsyncMock,
):
    """Step 7: goal.deadline ≠ standard.deadline → NOT_CONFIRMED."""
    goal_deadline = date(2026, 12, 1)
    premise1 = _make_premise(
        category=PremiseCategory.CONTRACT,
        data={
            "deadline": {"value": "2026-12-01", "owner": "contract", "source": None},
        },
        name="Договор",
    )
    premise2 = _make_premise(
        category=PremiseCategory.TZ,
        data={
            "requirement": {
                "value": "Сдать том 7",
                "owner": "tz",
                "source": None,
            },
        },
        name="ТЗ",
    )
    goal = _make_goal(
        premise_ids=[premise1.id, premise2.id],
        deadline=goal_deadline,
    )
    mock_goal_repo.get_by_id.return_value = goal
    mock_premise_repo.get_by_id.side_effect = [premise1, premise2]

    std = ProjectStandard(
        id=uuid4(),
        premise_id=uuid4(),
        type=ProjectStandardType.DEADLINE,
        value={"deadline": "2026-06-01"},
    )
    mock_standard_repo.list_by_goal.return_value = [std]
    mock_result_repo.list_by_goal.return_value = [
        Result(id=uuid4(), project_id=uuid4(), formulation="Result")
    ]

    result = await service.validate(goal.id)

    assert result.verification_status == VerificationStatus.NOT_CONFIRMED
    assert any(
        "deadline mismatch" in c for c in result.contradictions
    )
