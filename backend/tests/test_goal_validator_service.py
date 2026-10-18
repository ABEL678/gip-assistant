"""Тесты GoalValidatorService."""

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
from backend.src.domain.services.goal_validator_service import (
    GoalValidatorService,
)
from backend.src.domain.value_objects.enums import (
    PremiseCategory,
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
    return repo


@pytest.fixture
def service(
    mock_goal_repo: AsyncMock, mock_premise_repo: AsyncMock
) -> GoalValidatorService:
    return GoalValidatorService(mock_goal_repo, mock_premise_repo)


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
    service: GoalValidatorService,
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
    service: GoalValidatorService,
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
    service: GoalValidatorService,
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
    service: GoalValidatorService,
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
    service: GoalValidatorService,
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
    service: GoalValidatorService,
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
    service: GoalValidatorService,
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
    service: GoalValidatorService,
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
    service: GoalValidatorService,
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
