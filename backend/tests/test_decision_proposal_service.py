"""Тесты DecisionProposalService."""

from datetime import date
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from backend.src.domain.entities.decision import Decision
from backend.src.domain.entities.goal import Goal
from backend.src.domain.services.decision_proposal_service import (
    DecisionProposalService,
)
from backend.src.domain.value_objects.enums import DecisionState


@pytest.fixture
def mock_goal_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.list_by_project = AsyncMock()
    repo.save = AsyncMock()
    return repo


@pytest.fixture
def mock_decision_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.list_by_project = AsyncMock()
    repo.save = AsyncMock()
    return repo


@pytest.fixture
def service(
    mock_goal_repo: AsyncMock, mock_decision_repo: AsyncMock,
) -> DecisionProposalService:
    return DecisionProposalService(mock_goal_repo, mock_decision_repo)


@pytest.fixture
def project_id() -> UUID:
    return uuid4()


def _make_goal(project_id: UUID, **kwargs) -> Goal:
    return Goal(project_id=project_id, formulation="Сдать том 7 в экспертизу", **kwargs)


# ---------- Правило 1: goal_без_решения ----------


@pytest.mark.asyncio
async def test_rule_goal_without_decision(
    service: DecisionProposalService,
    mock_goal_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    project_id: UUID,
):
    """Правило 1 — Goal без Decision → «Определить способ реализации»."""
    goal = _make_goal(project_id)
    mock_goal_repo.list_by_project.return_value = [goal]
    mock_decision_repo.list_by_project.return_value = []

    proposals = await service.propose_decisions(project_id)

    assert len(proposals) == 1
    p = proposals[0]
    assert p.rule == "goal_без_решения"
    assert p.formulation == "Определить способ реализации цели: Сдать том 7 в экспертизу"
    assert p.goal_ids == [goal.id]
    assert p.premise_ids == []
    assert p.state == DecisionState.PLAN


@pytest.mark.asyncio
async def test_rule_goal_with_decision_not_fired(
    service: DecisionProposalService,
    mock_goal_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    project_id: UUID,
):
    """Правило 1 не срабатывает, если у Goal уже есть Decision."""
    goal = _make_goal(project_id)
    decision = Decision(project_id=project_id, formulation="Есть решение")
    decision.goal_ids = [goal.id]
    mock_goal_repo.list_by_project.return_value = [goal]
    mock_decision_repo.list_by_project.return_value = [decision]

    proposals = await service.propose_decisions(project_id)

    assert proposals == []


# ---------- Правило 2: срок_из_вводных ----------


@pytest.mark.asyncio
async def test_rule_deadline_from_premises(
    service: DecisionProposalService,
    mock_goal_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    project_id: UUID,
):
    """Правило 2 — Goal с deadline и premise_ids → «Обосновать срок»."""
    premise_id = uuid4()
    goal = _make_goal(project_id, deadline=date(2026, 12, 1), premise_ids=[premise_id])
    # Решение уже есть — правило 1 не должно сработать
    decision = Decision(project_id=project_id, formulation="Есть решение")
    decision.goal_ids = [goal.id]
    mock_goal_repo.list_by_project.return_value = [goal]
    mock_decision_repo.list_by_project.return_value = [decision]

    proposals = await service.propose_decisions(project_id)

    assert len(proposals) == 1
    p = proposals[0]
    assert p.rule == "срок_из_вводных"
    assert p.formulation == "Обосновать срок: Сдать том 7 в экспертизу"
    assert p.rationale == "Срок 2026-12-01 из вводных"
    assert p.premise_ids == [premise_id]
    assert p.goal_ids == [goal.id]
    assert p.state == DecisionState.PLAN


@pytest.mark.asyncio
async def test_rule_deadline_not_fired_without_deadline(
    service: DecisionProposalService,
    mock_goal_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    project_id: UUID,
):
    """Правило 2 не срабатывает без deadline."""
    goal = _make_goal(project_id, premise_ids=[uuid4()])
    decision = Decision(project_id=project_id, formulation="Есть решение")
    decision.goal_ids = [goal.id]
    mock_goal_repo.list_by_project.return_value = [goal]
    mock_decision_repo.list_by_project.return_value = [decision]

    proposals = await service.propose_decisions(project_id)

    assert proposals == []


@pytest.mark.asyncio
async def test_rule_deadline_not_fired_without_premises(
    service: DecisionProposalService,
    mock_goal_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    project_id: UUID,
):
    """Правило 2 не срабатывает без premise_ids."""
    goal = _make_goal(project_id, deadline=date(2026, 12, 1))
    decision = Decision(project_id=project_id, formulation="Есть решение")
    decision.goal_ids = [goal.id]
    mock_goal_repo.list_by_project.return_value = [goal]
    mock_decision_repo.list_by_project.return_value = [decision]

    proposals = await service.propose_decisions(project_id)

    assert proposals == []


# ---------- Оба правила вместе ----------


@pytest.mark.asyncio
async def test_both_rules_two_proposals_no_dedup(
    service: DecisionProposalService,
    mock_goal_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    project_id: UUID,
):
    """Один Goal без решения и с дедлайном → 2 предложения, без дедупликации."""
    premise_id = uuid4()
    goal = _make_goal(project_id, deadline=date(2026, 12, 1), premise_ids=[premise_id])
    mock_goal_repo.list_by_project.return_value = [goal]
    mock_decision_repo.list_by_project.return_value = []

    proposals = await service.propose_decisions(project_id)

    assert len(proposals) == 2
    assert {p.rule for p in proposals} == {"goal_без_решения", "срок_из_вводных"}
    assert all(p.goal_ids == [goal.id] for p in proposals)


# ---------- Общие свойства ----------


@pytest.mark.asyncio
async def test_empty_project(
    service: DecisionProposalService,
    mock_goal_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    project_id: UUID,
):
    """Нет целей — нет предложений."""
    mock_goal_repo.list_by_project.return_value = []
    mock_decision_repo.list_by_project.return_value = []

    proposals = await service.propose_decisions(project_id)

    assert proposals == []


@pytest.mark.asyncio
async def test_no_persistence(
    service: DecisionProposalService,
    mock_goal_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    project_id: UUID,
):
    """Предложения не сохраняются в БД (DOMAIN.md §2: ГИП утверждает)."""
    goal = _make_goal(project_id)
    mock_goal_repo.list_by_project.return_value = [goal]
    mock_decision_repo.list_by_project.return_value = []

    await service.propose_decisions(project_id)

    mock_goal_repo.save.assert_not_called()
    mock_decision_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_proposal_ids_generated_and_deterministic(
    service: DecisionProposalService,
    mock_goal_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    project_id: UUID,
):
    """Каждому предложению присваивается детерминированный id (UI key)."""
    goal = _make_goal(project_id)
    mock_goal_repo.list_by_project.return_value = [goal]
    mock_decision_repo.list_by_project.return_value = []

    first = await service.propose_decisions(project_id)
    second = await service.propose_decisions(project_id)

    assert all(p.id is not None for p in first)
    assert [p.id for p in first] == [p.id for p in second]
