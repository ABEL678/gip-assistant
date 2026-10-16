"""Тесты репозитория Goal (mock-based)."""

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from backend.src.adapters.db.models.goal import GoalModel
from backend.src.adapters.db.repositories.goal_repository import (
    SqlAlchemyGoalRepository,
)
from backend.src.domain.entities.goal import Goal
from backend.src.domain.value_objects.enums import GoalState


@pytest.fixture
def mock_session() -> AsyncMock:
    """Мокированный AsyncSession."""
    session = AsyncMock()
    session.merge = AsyncMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    session.add = AsyncMock()
    return session


@pytest.fixture
def repo(mock_session: AsyncMock) -> SqlAlchemyGoalRepository:
    return SqlAlchemyGoalRepository(mock_session)


@pytest.fixture
def goal() -> Goal:
    return Goal(
        id=uuid4(),
        project_id=uuid4(),
        formulation="Сдать том 7 в экспертизу",
        state=GoalState.PLAN,
        priority=3,
        premise_ids=[uuid4(), uuid4()],
    )


@pytest.fixture
def goal_model(goal: Goal) -> GoalModel:
    return SqlAlchemyGoalRepository._to_model(goal)


@pytest.mark.asyncio
async def test_get_by_id_found(repo: SqlAlchemyGoalRepository, mock_session: AsyncMock, goal: Goal):
    """get_by_id — находит цель по ID."""
    mock_session.get.return_value = SqlAlchemyGoalRepository._to_model(goal)

    result = await repo.get_by_id(goal.id)

    assert result is not None
    assert result.id == goal.id
    assert result.state == GoalState.PLAN
    mock_session.get.assert_called_once()


@pytest.mark.asyncio
async def test_get_by_id_not_found(repo: SqlAlchemyGoalRepository, mock_session: AsyncMock):
    """get_by_id — возвращает None если не найдена."""
    mock_session.get.return_value = None

    result = await repo.get_by_id(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_list_by_project(repo: SqlAlchemyGoalRepository, mock_session: AsyncMock, goal: Goal):
    """list_by_project — возвращает список целей проекта."""
    project_id = goal.project_id
    model = SqlAlchemyGoalRepository._to_model(goal)

    result_mock = MagicMock()
    result_mock.scalars().all.return_value = [model]
    mock_session.execute.return_value = result_mock

    result = await repo.list_by_project(project_id)

    assert len(result) == 1
    assert result[0].id == goal.id
    assert result[0].formulation == goal.formulation


@pytest.mark.asyncio
async def test_save_create(repo: SqlAlchemyGoalRepository, mock_session: AsyncMock, goal: Goal):
    """save — создаёт новую цель (merge)."""
    model = SqlAlchemyGoalRepository._to_model(goal)
    mock_session.merge.return_value = model
    mock_session.refresh = AsyncMock()

    result = await repo.save(goal)

    assert result.id == goal.id
    mock_session.merge.assert_called_once()
    assert mock_session.flush.call_count >= 1


@pytest.mark.asyncio
async def test_save_with_premise_ids(repo: SqlAlchemyGoalRepository, mock_session: AsyncMock, goal: Goal):
    """save — сохраняет связи goal_premises если premise_ids не пусто."""
    model = SqlAlchemyGoalRepository._to_model(goal)
    model.id = goal.id  # merge возвращает модель с ID
    mock_session.merge.return_value = model
    mock_session.refresh = AsyncMock()

    await repo.save(goal)

    # Проверяем что execute был вызван для удаления старых связей
    assert mock_session.execute.called
    # Проверяем что add был вызван для новых связей
    assert mock_session.add.call_count == len(goal.premise_ids)


@pytest.mark.asyncio
async def test_delete(repo: SqlAlchemyGoalRepository, mock_session: AsyncMock, goal: Goal):
    """delete — удаляет цель по ID."""
    result_mock = MagicMock()
    mock_session.execute.return_value = result_mock

    await repo.delete(goal.id)

    mock_session.execute.assert_called_once()
    mock_session.flush.assert_called_once()
