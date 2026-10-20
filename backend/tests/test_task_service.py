"""Тесты TaskService."""

from datetime import date
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from backend.src.domain.entities.task import Task
from backend.src.domain.ports.repositories import TaskRepository
from backend.src.domain.services.task_service import TaskService
from backend.src.domain.value_objects.enums import TaskStatus


@pytest.fixture
def mock_task_repo() -> AsyncMock:
    repo = AsyncMock(spec=TaskRepository)
    repo.get_by_id = AsyncMock()
    repo.get_by_project = AsyncMock()
    repo.save = AsyncMock()
    repo.delete = AsyncMock()
    return repo


@pytest.fixture
def service(mock_task_repo: AsyncMock) -> TaskService:
    return TaskService(mock_task_repo)


@pytest.fixture
def valid_task() -> Task:
    return Task(
        id=uuid4(),
        project_id=uuid4(),
        title="Проверить проект",
        is_complex=False,
    )


@pytest.mark.asyncio
async def test_create_with_is_complex_true(
    service: TaskService, mock_task_repo: AsyncMock,
):
    """create с is_complex=True → сохраняется True."""
    project_id = uuid4()
    saved_task = Task(
        id=uuid4(),
        project_id=project_id,
        title="Комплексная задача",
        is_complex=True,
    )
    mock_task_repo.save.return_value = saved_task

    result = await service.create(
        project_id=project_id,
        title="Комплексная задача",
        is_complex=True,
    )

    assert result.is_complex is True
    mock_task_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_update_with_is_complex_true(
    service: TaskService, mock_task_repo: AsyncMock, valid_task: Task,
):
    """update с is_complex=True → меняется."""
    mock_task_repo.get_by_id.return_value = valid_task
    mock_task_repo.save.return_value = valid_task

    result = await service.update(valid_task.id, is_complex=True)

    assert result.is_complex is True
    mock_task_repo.save.assert_called_once()
