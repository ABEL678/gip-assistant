"""RfiProposalService — 2 правила (spec_week_4.md §6)."""

from datetime import date, datetime, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from backend.src.application.dto.rfi import RfiProposal
from backend.src.domain.entities.decision import Decision
from backend.src.domain.entities.task import Task
from backend.src.domain.services.rfi_proposal_service import (
    DECISION_AGE_DAYS,
    RfiProposalService,
)


@pytest.mark.asyncio
async def test_decision_without_ids_old_no_premises():
    """Decision без Premise > 5д → предлагает create."""
    project_id = uuid4()
    decision_id = uuid4()
    created = date.today() - timedelta(days=DECISION_AGE_DAYS + 1)
    decision = Decision(
        project_id=project_id,
        formulation="Передать расчёт ВК",
        state="plan",
        premise_ids=[],
        created_at=datetime(created.year, created.month, created.day),
    )
    decision.id = decision_id
    decision_repo = AsyncMock()
    decision_repo.list_by_project.return_value = [decision]
    rfi_repo = AsyncMock()
    rfi_repo.list_overdue.return_value = []

    service = RfiProposalService(decision_repo=decision_repo, rfi_repo=rfi_repo)
    proposals = await service.propose_rfis(project_id)
    create_proposals = [p for p in proposals if isinstance(p, RfiProposal) and p.action == "create"]
    assert len(create_proposals) == 1
    assert create_proposals[0].rule == "decision_без_ид"

    rfi_repo.list_overdue.assert_called_once_with(
        date.today(), project_id
    )


@pytest.mark.asyncio
async def test_decision_without_ids_has_premises():
    """Decision с Premise → не предлагает."""
    project_id = uuid4()
    decision = Decision(
        project_id=project_id,
        formulation="Передать расчёт",
        state="plan",
        premise_ids=[uuid4()],
    )
    decision_repo = AsyncMock()
    decision_repo.list_by_project.return_value = [decision]
    rfi_repo = AsyncMock()
    rfi_repo.list_overdue.return_value = []

    service = RfiProposalService(decision_repo=decision_repo, rfi_repo=rfi_repo)
    proposals = await service.propose_rfis(project_id)
    create_proposals = [p for p in proposals if isinstance(p, RfiProposal) and p.action == "create"]
    assert len(create_proposals) == 0


@pytest.mark.asyncio
async def test_decision_without_ids_too_young():
    """Decision моложе 5д → не предлагает."""
    project_id = uuid4()
    decision = Decision(
        project_id=project_id,
        formulation="Новое решение",
        state="plan",
        premise_ids=[],
        created_at=datetime.now(),
    )
    decision_repo = AsyncMock()
    decision_repo.list_by_project.return_value = [decision]
    rfi_repo = AsyncMock()
    rfi_repo.list_overdue.return_value = []

    service = RfiProposalService(decision_repo=decision_repo, rfi_repo=rfi_repo)
    proposals = await service.propose_rfis(project_id)
    create_proposals = [p for p in proposals if isinstance(p, RfiProposal) and p.action == "create"]
    assert len(create_proposals) == 0


@pytest.mark.asyncio
async def test_rfi_overdue():
    """Просроченный RFI → предлагает escalate."""
    project_id = uuid4()
    rfi = Task(
        project_id=project_id,
        title="Старый RFI",
        is_rfi=True,
        rfi_due_date=date.today() - timedelta(days=3),
        rfi_state="open",
    )
    rfi_repo = AsyncMock()
    rfi_repo.list_overdue.return_value = [rfi]
    decision_repo = AsyncMock()
    decision_repo.list_by_project.return_value = []

    service = RfiProposalService(decision_repo=decision_repo, rfi_repo=rfi_repo)
    proposals = await service.propose_rfis(project_id)
    escalate_proposals = [p for p in proposals if isinstance(p, RfiProposal) and p.action == "escalate"]
    assert len(escalate_proposals) == 1
    assert escalate_proposals[0].rule == "rfi_просрочен"


@pytest.mark.asyncio
async def test_rfi_closed_not_overdue():
    """Закрытый RFI в списке overdue → сервис фильтрует."""
    project_id = uuid4()
    closed_rfi = Task(
        project_id=project_id,
        title="Закрытый RFI",
        is_rfi=True,
        rfi_due_date=date.today() - timedelta(days=3),
        rfi_state="closed",
    )
    # Репозиторий возвращает closed RFI (фильтр репо не отфильтровал)
    rfi_repo = AsyncMock()
    rfi_repo.list_overdue.return_value = [closed_rfi]
    decision_repo = AsyncMock()
    decision_repo.list_by_project.return_value = []

    service = RfiProposalService(decision_repo=decision_repo, rfi_repo=rfi_repo)
    proposals = await service.propose_rfis(project_id)
    # Правило 2 должно отфильтровать closed RFI
    assert len(proposals) == 0


@pytest.mark.asyncio
async def test_rfi_not_overdue():
    """Непросроченный RFI → не предлагает."""
    project_id = uuid4()
    future_rfi = Task(
        project_id=project_id,
        title="Актуальный RFI",
        is_rfi=True,
        rfi_due_date=date.today() + timedelta(days=5),
        rfi_state="open",
    )
    rfi_repo = AsyncMock()
    rfi_repo.list_overdue.return_value = [future_rfi]
    decision_repo = AsyncMock()
    decision_repo.list_by_project.return_value = []

    service = RfiProposalService(decision_repo=decision_repo, rfi_repo=rfi_repo)
    proposals = await service.propose_rfis(project_id)
    # future_rfi в списке overdue → guard _rule_rfi_overdue отфильтрует
    assert len(proposals) == 0


@pytest.mark.asyncio
async def test_cross_project_rfi_not_in_proposals():
    """RFI из другого проекта → не попадает в propose_rfis."""
    project_id = uuid4()
    rfi_repo = AsyncMock()
    # Репозиторий с project_id фильтром вернёт пустой список
    rfi_repo.list_overdue.return_value = []
    decision_repo = AsyncMock()
    decision_repo.list_by_project.return_value = []

    service = RfiProposalService(decision_repo=decision_repo, rfi_repo=rfi_repo)
    proposals = await service.propose_rfis(project_id)

    # list_overdue должен был вызван с project_id
    rfi_repo.list_overdue.assert_called_once_with(
        date.today(), project_id
    )
    assert len(proposals) == 0
