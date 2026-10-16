"""Тесты GoalService."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from backend.src.domain.entities.goal import Goal
from backend.src.domain.services.goal_service import GoalService
from backend.src.domain.value_objects.enums import GoalState


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
    return repo


@pytest.fixture
def service(mock_goal_repo: AsyncMock, mock_premise_repo: AsyncMock) -> GoalService:
    return GoalService(mock_goal_repo, mock_premise_repo)


@pytest.fixture
def valid_goal() -> Goal:
    return Goal(
        id=uuid4(),
        project_id=uuid4(),
        formulation="Сдать том 7 в экспертизу",
        state=GoalState.PLAN,
    )


@pytest.mark.asyncio
async def test_get(service: GoalService, mock_goal_repo: AsyncMock, valid_goal: Goal):
    """get — находит цель по ID."""
    mock_goal_repo.get_by_id.return_value = valid_goal

    result = await service.get(valid_goal.id)

    assert result is valid_goal


@pytest.mark.asyncio
async def test_get_not_found(service: GoalService, mock_goal_repo: AsyncMock):
    """get — возвращает None если не найдена."""
    mock_goal_repo.get_by_id.return_value = None

    result = await service.get(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_list_by_project(service: GoalService, mock_goal_repo: AsyncMock, valid_goal: Goal):
    """list_by_project — возвращает список целей."""
    project_id = valid_goal.project_id
    mock_goal_repo.list_by_project.return_value = [valid_goal]

    result = await service.list_by_project(project_id)

    assert len(result) == 1
    assert result[0].id == valid_goal.id


@pytest.mark.asyncio
async def test_create_success(service: GoalService, mock_goal_repo: AsyncMock):
    """create — создаёт цель при успешной валидации."""
    mock_goal_repo.save.return_value = Goal(
        id=uuid4(),
        project_id=uuid4(),
        formulation="Новая цель",
    )

    result = await service.create(
        project_id=uuid4(),
        formulation="Новая цель",
    )

    assert result.formulation == "Новая цель"
    mock_goal_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_empty_formulation(service: GoalService, mock_goal_repo: AsyncMock):
    """create — пустая формулировка → ValueError."""
    with pytest.raises(ValueError, match="не может быть пустой"):
        await service.create(
            project_id=uuid4(),
            formulation="   ",
        )
    mock_goal_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_with_premise_ids_not_found(
    service: GoalService, mock_goal_repo: AsyncMock, mock_premise_repo: AsyncMock,
):
    """create — несуществующий premise_id → ValueError."""
    mock_premise_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найдена"):
        await service.create(
            project_id=uuid4(),
            formulation="Цель",
            premise_ids=[uuid4()],
        )


@pytest.mark.asyncio
async def test_update_success(service: GoalService, mock_goal_repo: AsyncMock, valid_goal: Goal):
    """update — обновляет существующую цель."""
    mock_goal_repo.get_by_id.return_value = valid_goal
    mock_goal_repo.save.return_value = valid_goal

    result = await service.update(valid_goal.id, state=GoalState.IN_PROGRESS)

    assert result.state == GoalState.IN_PROGRESS


@pytest.mark.asyncio
async def test_update_not_found(service: GoalService, mock_goal_repo: AsyncMock):
    """update — несуществующая цель → ValueError."""
    mock_goal_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найдена"):
        await service.update(uuid4())


@pytest.mark.asyncio
async def test_delete_success(service: GoalService, mock_goal_repo: AsyncMock, valid_goal: Goal):
    """delete — удаляет существующую цель."""
    mock_goal_repo.get_by_id.return_value = valid_goal

    await service.delete(valid_goal.id)

    mock_goal_repo.delete.assert_called_once_with(valid_goal.id)


@pytest.mark.asyncio
async def test_delete_not_found(service: GoalService, mock_goal_repo: AsyncMock):
    """delete — несуществующая цель → ValueError."""
    mock_goal_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найдена"):
        await service.delete(uuid4())
