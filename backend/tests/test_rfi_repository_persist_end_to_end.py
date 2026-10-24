"""Unit-тест persist RFI Task через AsyncMock (6.12a)."""

from datetime import date
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from backend.src.adapters.db.repositories.task_repo import SqlAlchemyTaskRepository
from backend.src.domain.entities.task import Task
from backend.src.domain.value_objects.enums import RfiState, TaskStatus


@pytest.fixture
def rfi_task():
    """RFI Task с заполненными rfi-полями."""
    return Task(
        project_id=uuid4(),
        title="Запросить ИД для решения",
        is_rfi=True,
        rfi_cause_decision_id=uuid4(),
        rfi_cause_goal_id=None,
        rfi_due_date=date(2026, 12, 31),
        rfi_state=RfiState.OPEN,
        status=TaskStatus.NOT_STARTED,
    )


@pytest.fixture
def mock_session():
    """Мок сессии с моками merge/flush/refresh."""
    session = AsyncMock()
    model = MagicMock()
    session.merge.return_value = model
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    return session


@pytest.mark.asyncio
async def test_rfi_task_save_and_get(mock_session, rfi_task):
    """RFI Task: save → проверка 5 полей.
    premise_ids — placeholder в 6.12a; контракт (непустой) —
    test_rfi_premise_ids_persist_end_to_end в 6.12b.
    """
    # Настройка мока: merge возвращает модель с нужными полями
    model = MagicMock()
    model.is_rfi = True
    model.rfi_cause_decision_id = rfi_task.rfi_cause_decision_id
    model.rfi_cause_goal_id = None
    model.rfi_due_date = rfi_task.rfi_due_date
    model.rfi_state = "open"
    model.project_id = rfi_task.project_id
    model.title = rfi_task.title
    model.status = rfi_task.status
    model.created_at = None
    model.updated_at = None

    mock_session.merge.return_value = model
    mock_session.flush = AsyncMock()
    mock_session.refresh = AsyncMock()

    # _fetch_premise_ids делает execute() → вернуть пустой список premise_ids
    mock_result = MagicMock()
    mock_result.scalars().all.return_value = []
    mock_session.execute = AsyncMock(return_value=mock_result)

    repo = SqlAlchemyTaskRepository(mock_session)
    result = await repo.save(rfi_task)
    assert result.is_rfi is True
    assert result.rfi_state == RfiState.OPEN
    assert result.rfi_cause_decision_id == rfi_task.rfi_cause_decision_id
    assert result.rfi_due_date == rfi_task.rfi_due_date


@pytest.mark.asyncio
async def test_rfi_task_save_non_rfi(mock_session):
    """Не-RFI Task: save → is_rfi=False, rfi_state=None."""
    model = MagicMock()
    model.is_rfi = False
    model.rfi_state = None
    model.rfi_cause_decision_id = None
    model.rfi_cause_goal_id = None
    model.rfi_due_date = None
    model.project_id = uuid4()
    model.title = "обычная задача"
    model.status = "IN_PROGRESS"
    model.created_at = None
    model.updated_at = None

    mock_session.merge.return_value = model
    mock_session.flush = AsyncMock()
    mock_session.refresh = AsyncMock()

    task = Task(
        project_id=uuid4(),
        title="обычная задача",
        status=TaskStatus.IN_PROGRESS,
    )
    repo = SqlAlchemyTaskRepository(mock_session)
    result = await repo.save(task)
    assert result.is_rfi is False
    assert result.rfi_state is None
    assert result.rfi_cause_decision_id is None


@pytest.mark.asyncio
async def test_rfi_task_get_by_id(mock_session, rfi_task):
    """get_by_id: select → _to_domain → все поля на месте."""
    model_mock = MagicMock()
    model_mock.id = rfi_task.id
    model_mock.project_id = rfi_task.project_id
    model_mock.title = rfi_task.title
    model_mock.status = rfi_task.status
    model_mock.is_rfi = True
    model_mock.rfi_cause_decision_id = rfi_task.rfi_cause_decision_id
    model_mock.rfi_cause_goal_id = None
    model_mock.rfi_due_date = rfi_task.rfi_due_date
    model_mock.rfi_state = "sent"
    model_mock.created_at = None
    model_mock.updated_at = None

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = model_mock
    mock_session.execute = AsyncMock(return_value=mock_result)

    repo = SqlAlchemyTaskRepository(mock_session)
    result = await repo.get_by_id(rfi_task.id)
    assert result is not None
    assert result.is_rfi is True
    assert result.rfi_state == RfiState.SENT
    assert result.rfi_cause_decision_id == rfi_task.rfi_cause_decision_id
