"""Тесты SimilarityMatrixService."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from backend.src.domain.entities.premise import Premise
from backend.src.domain.services.similarity_matrix_service import (
    SimilarityMatrixService,
)
from backend.src.domain.value_objects.enums import PremiseCategory


@pytest.fixture
def mock_premise_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.list_by_project = AsyncMock()
    return repo


@pytest.fixture
def service(mock_premise_repo: AsyncMock) -> SimilarityMatrixService:
    return SimilarityMatrixService(mock_premise_repo)


# --- Helpers ---


def _make_premise(
    category: PremiseCategory = PremiseCategory.CONTRACT,
    data: dict | None = None,
    name: str = "Test Premise",
) -> Premise:
    return Premise(
        id=uuid4(),
        project_id=uuid4(),
        category=category,
        name=name,
        data=data or {},
    )


# --- Tests ---


@pytest.mark.asyncio
async def test_no_premises(
    service: SimilarityMatrixService,
    mock_premise_repo: AsyncMock,
):
    """Нет вводных → пустой список."""
    mock_premise_repo.list_by_project.return_value = []

    result = await service.find_links(uuid4())

    assert result == []


@pytest.mark.asyncio
async def test_one_section_only(
    service: SimilarityMatrixService,
    mock_premise_repo: AsyncMock,
):
    """Один раздел (АР) — нет пар → []."""
    premise = _make_premise(data={"sections": ["АР"]})
    mock_premise_repo.list_by_project.return_value = [premise]

    result = await service.find_links(uuid4())

    assert result == []


@pytest.mark.asyncio
async def test_two_sections_match(
    service: SimilarityMatrixService,
    mock_premise_repo: AsyncMock,
):
    """Два раздела (АР, ОВ) → 1 связь (АР↔ОВ)."""
    premise = _make_premise(data={"sections": ["АР", "ОВ"]})
    mock_premise_repo.list_by_project.return_value = [premise]

    result = await service.find_links(uuid4())

    assert len(result) == 1
    assert result[0].from_section == "АР"
    assert result[0].to_section == "ОВ"


@pytest.mark.asyncio
async def test_sections_from_sections_field(
    service: SimilarityMatrixService,
    mock_premise_repo: AsyncMock,
):
    """data={'sections': ['АР', 'КЖ']} → 1 связь (АР↔КЖ)."""
    premise = _make_premise(data={"sections": ["АР", "КЖ"]})
    mock_premise_repo.list_by_project.return_value = [premise]

    result = await service.find_links(uuid4())

    assert len(result) == 1
    assert result[0].from_section == "АР"
    assert result[0].to_section == "КЖ"


@pytest.mark.asyncio
async def test_sections_from_strings_in_data(
    service: SimilarityMatrixService,
    mock_premise_repo: AsyncMock,
):
    """Без sections: сканируем строковые значения data."""
    premise = _make_premise(
        data={
            "custom_field": "КЖ",
            "other": "значение",
        }
    )
    # Нужен второй раздел — добавим premise с АР
    premise2 = _make_premise(data={"sections": ["АР"]})
    mock_premise_repo.list_by_project.return_value = [premise, premise2]

    result = await service.find_links(uuid4())

    assert len(result) == 1
    assert result[0].from_section == "АР"
    assert result[0].to_section == "КЖ"


@pytest.mark.asyncio
async def test_priority_b_over_c(
    service: SimilarityMatrixService,
    mock_premise_repo: AsyncMock,
):
    """data={'sections': ['АР'], 'extra': 'ОВ'} → только АР (B приоритет)."""
    premise = _make_premise(data={"sections": ["АР"], "extra": "ОВ"})
    mock_premise_repo.list_by_project.return_value = [premise]

    result = await service.find_links(uuid4())

    # sections=['АР'] — только один раздел, нет пар
    assert result == []


@pytest.mark.asyncio
async def test_numbers_and_dates_skipped(
    service: SimilarityMatrixService,
    mock_premise_repo: AsyncMock,
):
    """Числа и даты не считаются разделами."""
    premise = _make_premise(
        data={
            "number": 5,
            "date": "2026-01-01",
        }
    )
    mock_premise_repo.list_by_project.return_value = [premise]

    result = await service.find_links(uuid4())

    assert result == []


@pytest.mark.asyncio
async def test_unknown_section_ignored(
    service: SimilarityMatrixService,
    mock_premise_repo: AsyncMock,
):
    """Раздел ГП не в MATRIX → []."""
    premise = _make_premise(data={"sections": ["ГП"]})
    mock_premise_repo.list_by_project.return_value = [premise]

    result = await service.find_links(uuid4())

    assert result == []


@pytest.mark.asyncio
async def test_non_relevant_category_ignored(
    service: SimilarityMatrixService,
    mock_premise_repo: AsyncMock,
):
    """Premise категории npa со списком разделов игнорируется."""
    premise = _make_premise(
        category=PremiseCategory.NPA,
        data={"sections": ["АР", "ОВ"]},
    )
    mock_premise_repo.list_by_project.return_value = [premise]

    result = await service.find_links(uuid4())

    assert result == []


@pytest.mark.asyncio
async def test_three_sections_three_links(
    service: SimilarityMatrixService,
    mock_premise_repo: AsyncMock,
):
    """АР, ОВ, КЖ → 3 связи (АР↔ОВ, АР↔КЖ, ОВ↔КЖ)."""
    premise = _make_premise(data={"sections": ["АР", "ОВ", "КЖ"]})
    mock_premise_repo.list_by_project.return_value = [premise]

    result = await service.find_links(uuid4())

    assert len(result) == 3
    pairs = {(l.from_section, l.to_section) for l in result}
    assert ("АР", "ОВ") in pairs
    assert ("АР", "КЖ") in pairs
    assert ("ОВ", "КЖ") in pairs
