"""Unit-тесты SqlAlchemyRfiRepository (AsyncMock на session.execute)."""

from datetime import date, timedelta
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from backend.src.adapters.db.models.task import Task as TaskModel
from backend.src.adapters.db.repositories.rfi_repository import (
    SqlAlchemyRfiRepository,
)
from backend.src.adapters.db.repositories.task_repo import (
    SqlAlchemyTaskRepository,
)
from backend.src.domain.value_objects.enums import RfiState, TaskStatus


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
def mock_task_repo(mock_session):
    repo = SqlAlchemyTaskRepository(mock_session)
    return repo


@pytest.fixture
def rfi_repo(mock_session, mock_task_repo):
    return SqlAlchemyRfiRepository(mock_session, mock_task_repo)


def _make_task_model(
    id=None,
    project_id=None,
    title="Test RFI",
    is_rfi=True,
    rfi_cause_decision_id=None,
    rfi_cause_goal_id=None,
    rfi_due_date=None,
    rfi_state=None,
    status=TaskStatus.NOT_STARTED,
):
    model = MagicMock(spec=TaskModel)
    model.id = id or uuid4()
    model.project_id = project_id or uuid4()
    model.title = title
    model.is_rfi = is_rfi
    model.rfi_cause_decision_id = rfi_cause_decision_id
    model.rfi_cause_goal_id = rfi_cause_goal_id
    model.rfi_due_date = rfi_due_date
    model.rfi_state = rfi_state
    model.status = status
    model.created_at = None
    model.updated_at = None
    return model


@pytest.mark.asyncio
async def test_list_rfis_by_project(rfi_repo, mock_session):
    """list_rfis_by_project — фильтрует is_rfi=true."""
    project_id = uuid4()
    rfi_model = _make_task_model(
        id=uuid4(), project_id=project_id, is_rfi=True
    )

    mock_result = MagicMock()
    mock_result.scalars().all.return_value = [rfi_model]
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Mock _fetch_premise_ids и _to_domain
    rfi_repo._task_repo._fetch_premise_ids = AsyncMock(return_value=[])
    rfi_repo._task_repo._to_domain = MagicMock(
        side_effect=lambda m, premise_ids: m
    )

    result = await rfi_repo.list_rfis_by_project(project_id)

    assert len(result) == 1
    mock_session.execute.assert_called_once()
    # Фильтры (project_id, due_date, state) покрыты интеграционно —
    # test_rfi_premise_ids_persist_end_to_end / 6.12c. Юнит-тесты проверяют обвязку (мок session.execute).


@pytest.mark.asyncio
async def test_get_rfi_by_found(rfi_repo, mock_session):
    """get_rfi_by_id — находит RFI по ID."""
    rfi_id = uuid4()
    rfi_model = _make_task_model(id=rfi_id, is_rfi=True)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = rfi_model
    mock_session.execute = AsyncMock(return_value=mock_result)

    rfi_repo._task_repo._fetch_premise_ids = AsyncMock(return_value=[])
    rfi_repo._task_repo._to_domain = MagicMock(
        side_effect=lambda m, premise_ids: m
    )

    result = await rfi_repo.get_rfi_by_id(rfi_id)

    assert result is not None
    assert result.id == rfi_id


@pytest.mark.asyncio
async def test_get_rfi_by_not_found(rfi_repo, mock_session):
    """get_rfi_by_id — не найден → None."""
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await rfi_repo.get_rfi_by_id(uuid4())
    assert result is None


@pytest.mark.asyncio
async def test_list_by_cause_decision(rfi_repo, mock_session):
    """list_by_cause_decision — фильтрует по decision_id."""
    decision_id = uuid4()
    rfi_model = _make_task_model(
        id=uuid4(),
        rfi_cause_decision_id=decision_id,
        is_rfi=True,
    )

    mock_result = MagicMock()
    mock_result.scalars().all.return_value = [rfi_model]
    mock_session.execute = AsyncMock(return_value=mock_result)

    rfi_repo._task_repo._fetch_premise_ids = AsyncMock(return_value=[])
    rfi_repo._task_repo._to_domain = MagicMock(
        side_effect=lambda m, premise_ids: m
    )

    result = await rfi_repo.list_by_cause_decision(decision_id)

    assert len(result) == 1


@pytest.mark.asyncio
async def test_list_by_cause_goal(rfi_repo, mock_session):
    """list_by_cause_goal — фильтрует по goal_id."""
    goal_id = uuid4()
    rfi_model = _make_task_model(
        id=uuid4(),
        rfi_cause_goal_id=goal_id,
        is_rfi=True,
    )

    mock_result = MagicMock()
    mock_result.scalars().all.return_value = [rfi_model]
    mock_session.execute = AsyncMock(return_value=mock_result)

    rfi_repo._task_repo._fetch_premise_ids = AsyncMock(return_value=[])
    rfi_repo._task_repo._to_domain = MagicMock(
        side_effect=lambda m, premise_ids: m
    )

    result = await rfi_repo.list_by_cause_goal(goal_id)

    assert len(result) == 1


@pytest.mark.asyncio
async def test_list_overdue(rfi_repo, mock_session):
    """list_overdue — фильтрует по due_date + project_id + state."""
    project_id = uuid4()
    rfi_model = _make_task_model(
        id=uuid4(),
        project_id=project_id,
        rfi_due_date=date.today() - timedelta(days=5),
        rfi_state=RfiState.OPEN,
    )

    mock_result = MagicMock()
    mock_result.scalars().all.return_value = [rfi_model]
    mock_session.execute = AsyncMock(return_value=mock_result)

    rfi_repo._task_repo._fetch_premise_ids = AsyncMock(return_value=[])
    rfi_repo._task_repo._to_domain = MagicMock(
        side_effect=lambda m, premise_ids: m
    )

    result = await rfi_repo.list_overdue(date.today(), project_id)

    assert len(result) == 1
