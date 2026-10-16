"""Тесты GoalProposalService — 4 правила вывода + дедупликация."""

from datetime import date, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from backend.src.domain.entities.goal_proposal import GoalProposal
from backend.src.domain.entities.premise import Premise
from backend.src.domain.services.goal_proposal_service import GoalProposalService
from backend.src.domain.value_objects.enums import PremiseCategory


@pytest.fixture
def mock_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.list_by_project = AsyncMock()
    return repo


@pytest.fixture
def service(mock_repo: AsyncMock) -> GoalProposalService:
    return GoalProposalService(mock_repo)


@pytest.fixture
def contract_premise() -> Premise:
    return Premise(
        id=uuid4(),
        project_id=uuid4(),
        category=PremiseCategory.CONTRACT,
        name="Том 7",
        data={"deadline": "2026-12-01"},
    )


@pytest.fixture
def tz_premise() -> Premise:
    return Premise(
        id=uuid4(),
        project_id=uuid4(),
        category=PremiseCategory.TZ,
        name="ТЗ на разработку",
        data={"requirement": "Расчёт ВК"},
    )


@pytest.fixture
def customer_req_premise() -> Premise:
    return Premise(
        id=uuid4(),
        project_id=uuid4(),
        category=PremiseCategory.CUSTOMER_REQUIREMENT,
        name="Требование Заказчика",
        data={"content": "Добавить раздел Х"},
    )


@pytest.fixture
def source_data_premise_expired() -> Premise:
    return Premise(
        id=uuid4(),
        project_id=uuid4(),
        category=PremiseCategory.SOURCE_DATA,
        name="Грунтовые условия",
        valid_until=date.today() - timedelta(days=10),
    )


@pytest.fixture
def source_data_premise_valid() -> Premise:
    return Premise(
        id=uuid4(),
        project_id=uuid4(),
        category=PremiseCategory.SOURCE_DATA,
        name="Геодезия",
        valid_until=date.today() + timedelta(days=30),
    )


# ---------- Правило 1: договор со сроком ----------


@pytest.mark.asyncio
async def test_rule_contract_serves(service: GoalProposalService, mock_repo: AsyncMock, contract_premise: Premise):
    """Правило 1 — срабатывает когда у договора есть deadline."""
    mock_repo.list_by_project.return_value = [contract_premise]

    proposals = await service.propose_goals(uuid4())

    assert len(proposals) == 1
    assert proposals[0].rule == "договор_срок"
    assert "Том 7" in proposals[0].formulation
    assert proposals[0].premise_ids == [contract_premise.id]


@pytest.mark.asyncio
async def test_rule_contract_no_deadline(service: GoalProposalService, mock_repo: AsyncMock):
    """Правило 1 — не срабатывает без deadline."""
    mock_repo.list_by_project.return_value = [
        Premise(
            id=uuid4(),
            project_id=uuid4(),
            category=PremiseCategory.CONTRACT,
            name="Без срока",
            data={},
        )
    ]

    proposals = await service.propose_goals(uuid4())

    rule_proposals = [p for p in proposals if p.rule == "договор_срок"]
    assert len(rule_proposals) == 0


# ---------- Правило 2: ТЗ с требованием ----------


@pytest.mark.asyncio
async def test_rule_tz_serves(service: GoalProposalService, mock_repo: AsyncMock, tz_premise: Premise):
    """Правило 2 — срабатывает когда в ТЗ есть requirement."""
    mock_repo.list_by_project.return_value = [tz_premise]

    proposals = await service.propose_goals(uuid4())

    assert len(proposals) == 1
    assert proposals[0].rule == "тз_требование"
    assert proposals[0].formulation == "Расчёт ВК"


@pytest.mark.asyncio
async def test_rule_tz_no_requirement(service: GoalProposalService, mock_repo: AsyncMock):
    """Правило 2 — не срабатывает без requirement."""
    mock_repo.list_by_project.return_value = [
        Premise(
            id=uuid4(),
            project_id=uuid4(),
            category=PremiseCategory.TZ,
            name="Пустое ТЗ",
            data={},
        )
    ]

    proposals = await service.propose_goals(uuid4())

    rule_proposals = [p for p in proposals if p.rule == "тз_требование"]
    assert len(rule_proposals) == 0


# ---------- Правило 3: требование Заказчика ----------


@pytest.mark.asyncio
async def test_rule_customer_req_serves(
    service: GoalProposalService, mock_repo: AsyncMock, customer_req_premise: Premise,
):
    """Правило 3 — срабатывает когда есть content."""
    mock_repo.list_by_project.return_value = [customer_req_premise]

    proposals = await service.propose_goals(uuid4())

    assert len(proposals) == 1
    assert proposals[0].rule == "требование_заказчика"
    assert proposals[0].formulation == "Добавить раздел Х"


@pytest.mark.asyncio
async def test_rule_customer_req_no_content(
    service: GoalProposalService, mock_repo: AsyncMock,
):
    """Правило 3 — не срабатывает без content."""
    mock_repo.list_by_project.return_value = [
        Premise(
            id=uuid4(),
            project_id=uuid4(),
            category=PremiseCategory.CUSTOMER_REQUIREMENT,
            name="Пустое требование",
            data={},
        )
    ]

    proposals = await service.propose_goals(uuid4())

    rule_proposals = [p for p in proposals if p.rule == "требование_заказчика"]
    assert len(rule_proposals) == 0


# ---------- Правило 4: просроченный ИД ----------


@pytest.mark.asyncio
async def test_rule_source_data_expired(
    service: GoalProposalService, mock_repo: AsyncMock, source_data_premise_expired: Premise,
):
    """Правило 4 — срабатывает когда ИД просрочен."""
    mock_repo.list_by_project.return_value = [source_data_premise_expired]

    proposals = await service.propose_goals(uuid4())

    assert len(proposals) == 1
    assert proposals[0].rule == "просроченный_ид"
    assert "Обновить" in proposals[0].formulation
    # deadline = valid_until + 30 дней
    expected_deadline = source_data_premise_expired.valid_until + timedelta(days=30)
    assert proposals[0].deadline == expected_deadline


@pytest.mark.asyncio
async def test_rule_source_data_not_expired(
    service: GoalProposalService, mock_repo: AsyncMock, source_data_premise_valid: Premise,
):
    """Правило 4 — не срабатывает когда ИД не просрочен."""
    mock_repo.list_by_project.return_value = [source_data_premise_valid]

    proposals = await service.propose_goals(uuid4())

    rule_proposals = [p for p in proposals if p.rule == "просроченный_ид"]
    assert len(rule_proposals) == 0


# ---------- Дедупликация ----------


@pytest.mark.asyncio
async def test_deduplication(service: GoalProposalService, mock_repo: AsyncMock):
    """Дедупликация — одинаковые формулировки объединяются в один proposal."""
    premise1 = Premise(
        id=uuid4(),
        project_id=uuid4(),
        category=PremiseCategory.CONTRACT,
        name="Том 7",
        data={"deadline": "2026-12-01"},
    )
    premise2 = Premise(
        id=uuid4(),
        project_id=uuid4(),
        category=PremiseCategory.TZ,
        name="ТЗ",
        data={"requirement": "Сдать Том 7 к 2026-12-01"},
    )
    mock_repo.list_by_project.return_value = [premise1, premise2]

    proposals = await service.propose_goals(uuid4())

    # Обе формулировки совпадают → дедупликация объединяет в 1 proposal
    assert len(proposals) == 1
    assert proposals[0].rule == "договор_срок"  # первый rule
    # premise_ids должны быть объединены
    assert len(proposals[0].premise_ids) == 2


@pytest.mark.asyncio
async def test_empty_premises(service: GoalProposalService, mock_repo: AsyncMock):
    """Пустой список Premise → пустой список предложений."""
    mock_repo.list_by_project.return_value = []

    proposals = await service.propose_goals(uuid4())

    assert proposals == []
