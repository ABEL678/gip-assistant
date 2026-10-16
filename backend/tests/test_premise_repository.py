"""Тесты репозитория Premise (mock-based)."""

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from backend.src.adapters.db.models.premise import PremiseModel
from backend.src.adapters.db.repositories.premise_repository import (
    SqlAlchemyPremiseRepository,
)
from backend.src.domain.entities.premise import Premise
from backend.src.domain.value_objects.enums import PremiseCategory


@pytest.fixture
def mock_session() -> AsyncMock:
    """Мокированный AsyncSession."""
    session = AsyncMock()
    session.merge = AsyncMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    return session


@pytest.fixture
def repo(mock_session: AsyncMock) -> SqlAlchemyPremiseRepository:
    return SqlAlchemyPremiseRepository(mock_session)


@pytest.fixture
def premise() -> Premise:
    return Premise(
        id=uuid4(),
        project_id=uuid4(),
        category=PremiseCategory.CONTRACT,
        name="Договор на разработку",
        source="Письмо №12",
        actual=True,
        mandatory=True,
    )


@pytest.fixture
def premise_model(premise: Premise) -> PremiseModel:
    return SqlAlchemyPremiseRepository._to_model(premise)


@pytest.mark.asyncio
async def test_get_by_id_found(repo: SqlAlchemyPremiseRepository, mock_session: AsyncMock, premise: Premise):
    """get_by_id — находит вводную по ID."""
    mock_session.get.return_value = SqlAlchemyPremiseRepository._to_model(premise)

    result = await repo.get_by_id(premise.id)

    assert result is not None
    assert result.id == premise.id
    assert result.category == PremiseCategory.CONTRACT
    mock_session.get.assert_called_once()


@pytest.mark.asyncio
async def test_get_by_id_not_found(repo: SqlAlchemyPremiseRepository, mock_session: AsyncMock):
    """get_by_id — возвращает None если не найдена."""
    mock_session.get.return_value = None

    result = await repo.get_by_id(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_list_by_project(repo: SqlAlchemyPremiseRepository, mock_session: AsyncMock, premise: Premise):
    """list_by_project — возвращает список вводных проекта."""
    project_id = premise.project_id
    model = SqlAlchemyPremiseRepository._to_model(premise)

    result_mock = MagicMock()
    result_mock.scalars().all.return_value = [model]
    mock_session.execute.return_value = result_mock

    result = await repo.list_by_project(project_id)

    assert len(result) == 1
    assert result[0].id == premise.id
    assert result[0].category == PremiseCategory.CONTRACT


@pytest.mark.asyncio
async def test_save_create(repo: SqlAlchemyPremiseRepository, mock_session: AsyncMock, premise: Premise):
    """save — создаёт новую вводную (merge)."""
    model = SqlAlchemyPremiseRepository._to_model(premise)
    mock_session.merge.return_value = model
    mock_session.refresh = AsyncMock()

    result = await repo.save(premise)

    assert result.id == premise.id
    mock_session.merge.assert_called_once()
    mock_session.flush.assert_called_once()


@pytest.mark.asyncio
async def test_delete(repo: SqlAlchemyPremiseRepository, mock_session: AsyncMock, premise: Premise):
    """delete — удаляет вводную по ID."""
    result_mock = MagicMock()
    mock_session.execute.return_value = result_mock

    await repo.delete(premise.id)

    mock_session.execute.assert_called_once()
    mock_session.flush.assert_called_once()
