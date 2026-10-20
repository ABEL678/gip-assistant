"""Тесты ActionService."""

from datetime import date
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from backend.src.domain.entities.action import Action
from backend.src.domain.ports.repositories import ActionRepository
from backend.src.domain.services.action_service import ActionService
from backend.src.domain.value_objects.enums import ActionState


@pytest.fixture
def mock_action_repo() -> AsyncMock:
    repo = AsyncMock(spec=ActionRepository)
    repo.get_by_id = AsyncMock()
    repo.list_by_task = AsyncMock()
    repo.list_by_project = AsyncMock()
    repo.save = AsyncMock()
    repo.delete = AsyncMock()
    return repo


@pytest.fixture
def service(mock_action_repo: AsyncMock) -> ActionService:
    return ActionService(mock_action_repo)


@pytest.fixture
def valid_action() -> Action:
    return Action(
        id=uuid4(),
        project_id=uuid4(),
        formulation="Проверить документацию",
        state=ActionState.PLAN,
    )


@pytest.mark.asyncio
async def test_get_found(
    service: ActionService, mock_action_repo: AsyncMock, valid_action: Action,
):
    """get_by_id — находит действие по ID."""
    mock_action_repo.get_by_id.return_value = valid_action

    result = await service.get_by_id(valid_action.id)

    assert result is valid_action


@pytest.mark.asyncio
async def test_get_not_found(
    service: ActionService, mock_action_repo: AsyncMock,
):
    """get_by_id — возвращает None если не найдено."""
    mock_action_repo.get_by_id.return_value = None

    result = await service.get_by_id(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_list_by_task(
    service: ActionService, mock_action_repo: AsyncMock, valid_action: Action,
):
    """list_by_task — возвращает список действий задачи."""
    mock_action_repo.list_by_task.return_value = [valid_action]

    result = await service.list_by_task(valid_action.id)

    assert len(result) == 1
    assert result[0].id == valid_action.id


@pytest.mark.asyncio
async def test_list_by_project(
    service: ActionService, mock_action_repo: AsyncMock, valid_action: Action,
):
    """list_by_project — возвращает список действий проекта."""
    project_id = valid_action.project_id
    mock_action_repo.list_by_project.return_value = [valid_action]

    result = await service.list_by_project(project_id)

    assert len(result) == 1
    assert result[0].project_id == project_id


@pytest.mark.asyncio
async def test_create_empty_formulation(
    service: ActionService, mock_action_repo: AsyncMock,
):
    """create — пустая формулировка → ValueError."""
    with pytest.raises(ValueError, match="не может быть пустой"):
        await service.create(
            project_id=uuid4(),
            formulation="   ",
        )
    mock_action_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_success(
    service: ActionService, mock_action_repo: AsyncMock,
):
    """create — создаёт действие при успешной валидации."""
    project_id = uuid4()
    saved_action = Action(
        id=uuid4(),
        project_id=project_id,
        formulation="Новое действие",
        deadline=date(2026, 12, 1),
    )
    mock_action_repo.save.return_value = saved_action

    result = await service.create(
        project_id=project_id,
        formulation="Новое действие",
        deadline=date(2026, 12, 1),
    )

    assert result.formulation == "Новое действие"
    assert result.deadline == date(2026, 12, 1)
    mock_action_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_update_not_found(
    service: ActionService, mock_action_repo: AsyncMock,
):
    """update — несуществующее действие → ValueError."""
    mock_action_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найдено"):
        await service.update(uuid4(), formulation="Updated")


@pytest.mark.asyncio
async def test_delete_not_found(
    service: ActionService, mock_action_repo: AsyncMock,
):
    """delete — несуществующее действие → ValueError."""
    mock_action_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найдено"):
        await service.delete(uuid4())
