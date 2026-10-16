"""Тесты PremiseService."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from backend.src.domain.entities.premise import Premise
from backend.src.domain.services.premise_service import PremiseService
from backend.src.domain.value_objects.enums import PremiseCategory


@pytest.fixture
def mock_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.list_by_project = AsyncMock()
    repo.save = AsyncMock()
    repo.delete = AsyncMock()
    return repo


@pytest.fixture
def service(mock_repo: AsyncMock) -> PremiseService:
    return PremiseService(mock_repo)


@pytest.fixture
def valid_premise() -> Premise:
    return Premise(
        id=uuid4(),
        project_id=uuid4(),
        category=PremiseCategory.CONTRACT,
        name="Договор на разработку",
    )


@pytest.mark.asyncio
async def test_get(service: PremiseService, mock_repo: AsyncMock, valid_premise: Premise):
    """get — находит вводную по ID."""
    mock_repo.get_by_id.return_value = valid_premise

    result = await service.get(valid_premise.id)

    assert result is valid_premise
    mock_repo.get_by_id.assert_called_once_with(valid_premise.id)


@pytest.mark.asyncio
async def test_get_not_found(service: PremiseService, mock_repo: AsyncMock):
    """get — возвращает None если не найдена."""
    mock_repo.get_by_id.return_value = None

    result = await service.get(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_list_by_project(service: PremiseService, mock_repo: AsyncMock, valid_premise: Premise):
    """list_by_project — возвращает список вводных."""
    project_id = valid_premise.project_id
    mock_repo.list_by_project.return_value = [valid_premise]

    result = await service.list_by_project(project_id)

    assert len(result) == 1
    assert result[0].id == valid_premise.id


@pytest.mark.asyncio
async def test_create_success(service: PremiseService, mock_repo: AsyncMock):
    """create — создаёт вводную при успешной валидации."""
    mock_repo.save.return_value = Premise(
        id=uuid4(),
        project_id=uuid4(),
        category=PremiseCategory.CONTRACT,
        name="Договор",
    )

    result = await service.create(
        project_id=uuid4(),
        category=PremiseCategory.CONTRACT,
        name="Договор",
    )

    assert result.name == "Договор"
    assert result.category == PremiseCategory.CONTRACT
    mock_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_empty_name(service: PremiseService, mock_repo: AsyncMock):
    """create — пустое имя → ValueError."""
    with pytest.raises(ValueError, match="не может быть пустым"):
        await service.create(
            project_id=uuid4(),
            category=PremiseCategory.CONTRACT,
            name="   ",
        )
    mock_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_update_success(service: PremiseService, mock_repo: AsyncMock, valid_premise: Premise):
    """update — обновляет существующую вводную."""
    mock_repo.get_by_id.return_value = valid_premise
    mock_repo.save.return_value = valid_premise

    result = await service.update(valid_premise.id, name="Новое название")

    assert result.name == "Новое название"
    mock_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_update_not_found(service: PremiseService, mock_repo: AsyncMock):
    """update — несуществующая вводная → ValueError."""
    mock_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найдена"):
        await service.update(uuid4())


@pytest.mark.asyncio
async def test_delete_success(service: PremiseService, mock_repo: AsyncMock, valid_premise: Premise):
    """delete — удаляет существующую вводную."""
    mock_repo.get_by_id.return_value = valid_premise

    await service.delete(valid_premise.id)

    mock_repo.delete.assert_called_once_with(valid_premise.id)


@pytest.mark.asyncio
async def test_delete_not_found(service: PremiseService, mock_repo: AsyncMock):
    """delete — несуществующая вводная → ValueError."""
    mock_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найдена"):
        await service.delete(uuid4())
