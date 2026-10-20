"""Тесты ProjectStandardService."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from backend.src.domain.entities.project_standard import ProjectStandard
from backend.src.domain.services.project_standard_service import ProjectStandardService
from backend.src.domain.value_objects.enums import ProjectStandardType


@pytest.fixture
def mock_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.list_by_premise = AsyncMock()
    repo.list_by_type = AsyncMock()
    repo.save = AsyncMock()
    repo.delete = AsyncMock()
    return repo


@pytest.fixture
def service(mock_repo: AsyncMock) -> ProjectStandardService:
    return ProjectStandardService(mock_repo)


@pytest.fixture
def valid_standard() -> ProjectStandard:
    return ProjectStandard(
        id=uuid4(),
        premise_id=uuid4(),
        type=ProjectStandardType.DEADLINE,
        value={"date": "2026-12-31"},
    )


@pytest.mark.asyncio
async def test_get_by_id(service: ProjectStandardService, mock_repo: AsyncMock, valid_standard: ProjectStandard):
    """get_by_id — находит стандарт по ID."""
    mock_repo.get_by_id.return_value = valid_standard

    result = await service.get_by_id(valid_standard.id)

    assert result is valid_standard
    mock_repo.get_by_id.assert_called_once_with(valid_standard.id)


@pytest.mark.asyncio
async def test_get_by_id_not_found(service: ProjectStandardService, mock_repo: AsyncMock):
    """get_by_id — возвращает None если не найден."""
    mock_repo.get_by_id.return_value = None

    result = await service.get_by_id(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_list_by_premise(service: ProjectStandardService, mock_repo: AsyncMock, valid_standard: ProjectStandard):
    """list_by_premise — возвращает список стандартов вводной."""
    premise_id = valid_standard.premise_id
    mock_repo.list_by_premise.return_value = [valid_standard]

    result = await service.list_by_premise(premise_id)

    assert len(result) == 1
    assert result[0].id == valid_standard.id


@pytest.mark.asyncio
async def test_list_by_type(service: ProjectStandardService, mock_repo: AsyncMock, valid_standard: ProjectStandard):
    """list_by_type — возвращает список стандартов по типу."""
    mock_repo.list_by_type.return_value = [valid_standard]

    result = await service.list_by_type(ProjectStandardType.DEADLINE)

    assert len(result) == 1
    assert result[0].type == ProjectStandardType.DEADLINE


@pytest.mark.asyncio
async def test_create_success(service: ProjectStandardService, mock_repo: AsyncMock):
    """create — создаёт стандарт проекта."""
    premise_id = uuid4()
    mock_repo.save.return_value = ProjectStandard(
        id=uuid4(),
        premise_id=premise_id,
        type=ProjectStandardType.DEADLINE,
        value={"date": "2026-12-31"},
    )

    result = await service.create(
        premise_id=premise_id,
        type=ProjectStandardType.DEADLINE,
        value={"date": "2026-12-31"},
    )

    assert result.type == ProjectStandardType.DEADLINE
    assert result.value == {"date": "2026-12-31"}
    mock_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_default_value(service: ProjectStandardService, mock_repo: AsyncMock):
    """create — value=None → пустой словарь."""
    premise_id = uuid4()
    mock_repo.save.return_value = ProjectStandard(
        id=uuid4(),
        premise_id=premise_id,
        type=ProjectStandardType.FORMAT,
        value={},
    )

    result = await service.create(
        premise_id=premise_id,
        type=ProjectStandardType.FORMAT,
    )

    assert result.value == {}
    mock_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_update_not_found(service: ProjectStandardService, mock_repo: AsyncMock):
    """update — несуществующий стандарт → ValueError."""
    mock_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найден"):
        await service.update(uuid4())


@pytest.mark.asyncio
async def test_delete_not_found(service: ProjectStandardService, mock_repo: AsyncMock):
    """delete — несуществующий стандарт → ValueError."""
    mock_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найден"):
        await service.delete(uuid4())
