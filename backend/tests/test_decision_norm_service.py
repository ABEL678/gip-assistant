"""Тесты DecisionNormService."""

from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from backend.src.domain.entities.decision import Decision
from backend.src.domain.entities.norm import Norm
from backend.src.domain.services.decision_norm_service import DecisionNormService
from backend.src.domain.value_objects.enums import NormType


@pytest.fixture
def mock_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.list_norms_by_decision = AsyncMock()
    repo.list_decisions_by_norm = AsyncMock()
    repo.link = AsyncMock()
    repo.unlink = AsyncMock()
    return repo


@pytest.fixture
def mock_decision_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    return repo


@pytest.fixture
def mock_norm_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    return repo


@pytest.fixture
def service(
    mock_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    mock_norm_repo: AsyncMock,
) -> DecisionNormService:
    return DecisionNormService(mock_repo, mock_decision_repo, mock_norm_repo)


@pytest.fixture
def project_id() -> UUID:
    return uuid4()


@pytest.fixture
def decision(project_id: UUID) -> Decision:
    return Decision(project_id=project_id, formulation="Принять схему субподряда")


@pytest.fixture
def norm(project_id: UUID) -> Norm:
    return Norm(
        project_id=project_id,
        code="ГОСТ Р 21.101-2026",
        title="Основные положения",
        norm_type=NormType.GOST,
    )


# ---------- Связывание ----------


@pytest.mark.asyncio
async def test_link_success(
    service: DecisionNormService,
    mock_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    mock_norm_repo: AsyncMock,
    decision: Decision,
    norm: Norm,
):
    """link — валидные решение и норма → связь создана."""
    mock_decision_repo.get_by_id.return_value = decision
    mock_norm_repo.get_by_id.return_value = norm

    await service.link(decision.id, norm.id)

    mock_repo.link.assert_called_once_with(decision.id, norm.id)


@pytest.mark.asyncio
async def test_link_decision_not_found(
    service: DecisionNormService,
    mock_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    decision: Decision,
    norm: Norm,
):
    """link — решение не найдено → ValueError."""
    mock_decision_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Решение .* не найдено"):
        await service.link(decision.id, norm.id)

    mock_repo.link.assert_not_called()


@pytest.mark.asyncio
async def test_link_norm_not_found(
    service: DecisionNormService,
    mock_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    mock_norm_repo: AsyncMock,
    decision: Decision,
    norm: Norm,
):
    """link — норма не найдена → ValueError."""
    mock_decision_repo.get_by_id.return_value = decision
    mock_norm_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Норма .* не найдена"):
        await service.link(decision.id, norm.id)

    mock_repo.link.assert_not_called()


@pytest.mark.asyncio
async def test_link_different_projects(
    service: DecisionNormService,
    mock_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    mock_norm_repo: AsyncMock,
    decision: Decision,
):
    """link — решение и норма из разных проектов → ValueError."""
    other_norm = Norm(
        project_id=uuid4(),
        code="СНиП 1.0",
        title="Чужая норма",
        norm_type=NormType.SNIP,
    )
    mock_decision_repo.get_by_id.return_value = decision
    mock_norm_repo.get_by_id.return_value = other_norm

    with pytest.raises(ValueError, match="разных проектов"):
        await service.link(decision.id, other_norm.id)

    mock_repo.link.assert_not_called()


@pytest.mark.asyncio
async def test_link_idempotent(
    service: DecisionNormService,
    mock_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    mock_norm_repo: AsyncMock,
    decision: Decision,
    norm: Norm,
):
    """link — повторная связь не ошибка (идемпотентность)."""
    mock_decision_repo.get_by_id.return_value = decision
    mock_norm_repo.get_by_id.return_value = norm

    await service.link(decision.id, norm.id)
    await service.link(decision.id, norm.id)

    assert mock_repo.link.call_count == 2


# ---------- Развязывание и списки ----------


@pytest.mark.asyncio
async def test_unlink(
    service: DecisionNormService, mock_repo: AsyncMock,
    decision: Decision, norm: Norm,
):
    """unlink — делегирует в репозиторий."""
    await service.unlink(decision.id, norm.id)

    mock_repo.unlink.assert_called_once_with(decision.id, norm.id)


@pytest.mark.asyncio
async def test_list_norms_by_decision(
    service: DecisionNormService, mock_repo: AsyncMock, decision: Decision,
):
    """list_norms_by_decision — делегирует в репозиторий."""
    norm_ids = [uuid4(), uuid4()]
    mock_repo.list_norms_by_decision.return_value = norm_ids

    result = await service.list_norms_by_decision(decision.id)

    assert result == norm_ids
    mock_repo.list_norms_by_decision.assert_called_once_with(decision.id)


@pytest.mark.asyncio
async def test_list_decisions_by_norm(
    service: DecisionNormService, mock_repo: AsyncMock, norm: Norm,
):
    """list_decisions_by_norm — делегирует в репозиторий."""
    decision_ids = [uuid4()]
    mock_repo.list_decisions_by_norm.return_value = decision_ids

    result = await service.list_decisions_by_norm(norm.id)

    assert result == decision_ids
    mock_repo.list_decisions_by_norm.assert_called_once_with(norm.id)
