"""Тесты ResultService."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from backend.src.domain.entities.result import Result
from backend.src.domain.services.result_service import ResultService


@pytest.fixture
def mock_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.list_by_project = AsyncMock()
    repo.save = AsyncMock()
    repo.delete = AsyncMock()
    return repo


@pytest.fixture
def service(mock_repo: AsyncMock) -> ResultService:
    return ResultService(mock_repo)


@pytest.fixture
def valid_result() -> Result:
    return Result(
        id=uuid4(),
        project_id=uuid4(),
        formulation="Выдать проектную документацию",
        source="Договор",
    )


@pytest.mark.asyncio
async def test_get_by_id(service: ResultService, mock_repo: AsyncMock, valid_result: Result):
    """get_by_id — находит результат по ID."""
    mock_repo.get_by_id.return_value = valid_result

    result = await service.get_by_id(valid_result.id)

    assert result is valid_result
    mock_repo.get_by_id.assert_called_once_with(valid_result.id)


@pytest.mark.asyncio
async def test_get_by_id_not_found(service: ResultService, mock_repo: AsyncMock):
    """get_by_id — возвращает None если не найден."""
    mock_repo.get_by_id.return_value = None

    result = await service.get_by_id(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_list_by_project(service: ResultService, mock_repo: AsyncMock, valid_result: Result):
    """list_by_project — возвращает список результатов."""
    project_id = valid_result.project_id
    mock_repo.list_by_project.return_value = [valid_result]

    result = await service.list_by_project(project_id)

    assert len(result) == 1
    assert result[0].id == valid_result.id


@pytest.mark.asyncio
async def test_create_success(service: ResultService, mock_repo: AsyncMock):
    """create — создаёт результат при успешной валидации."""
    project_id = uuid4()
    mock_repo.save.return_value = Result(
        id=uuid4(),
        project_id=project_id,
        formulation="Выдать проектную документацию",
        source="Договор",
    )

    result = await service.create(
        project_id=project_id,
        formulation="Выдать проектную документацию",
        source="Договор",
    )

    assert result.formulation == "Выдать проектную документацию"
    assert result.source == "Договор"
    mock_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_empty_formulation(service: ResultService, mock_repo: AsyncMock):
    """create — пустая формулировка → ValueError."""
    with pytest.raises(ValueError, match="не может быть пустой"):
        await service.create(project_id=uuid4(), formulation="   ")
    mock_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_update_not_found(service: ResultService, mock_repo: AsyncMock):
    """update — несуществующий результат → ValueError."""
    mock_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найден"):
        await service.update(uuid4())


@pytest.mark.asyncio
async def test_delete_not_found(service: ResultService, mock_repo: AsyncMock):
    """delete — несуществующий результат → ValueError."""
    mock_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найден"):
        await service.delete(uuid4())
