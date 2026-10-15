"""Тесты DocumentTypeService."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from backend.src.domain.entities.document_type import DocumentType
from backend.src.domain.services.document_type_service import DocumentTypeService


@pytest.fixture
def repo():
    return AsyncMock()


@pytest.fixture
def service(repo):
    return DocumentTypeService(repo)


# ---------- Успешные сценарии ----------


@pytest.mark.asyncio
async def test_create_minimal(repo, service):
    """Создание типа с минимальным набором полей."""
    repo.get_by_code.return_value = None
    repo.save.side_effect = lambda dt: dt

    result = await service.create(code="drawing", name="Чертёж")

    assert result.code == "drawing"
    assert result.name == "Чертёж"
    assert result.description is None
    assert result.gost_code is None
    repo.get_by_code.assert_called_once_with("drawing")
    repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_with_all_fields(repo, service):
    """Создание типа со всеми полями."""
    repo.get_by_code.return_value = None
    repo.save.side_effect = lambda dt: dt

    result = await service.create(
        code="pz",
        name="Пояснительная записка",
        description="ПЗ к чертежам",
        gost_code="ГОСТ Р 1234-2024",
    )

    assert result.code == "pz"
    assert result.name == "Пояснительная записка"
    assert result.description == "ПЗ к чертежам"
    assert result.gost_code == "ГОСТ Р 1234-2024"


@pytest.mark.asyncio
async def test_create_rejects_duplicate_code(repo, service):
    """Дубликат code → ValueError."""
    repo.get_by_code.return_value = DocumentType(code="drawing", name="X")

    with pytest.raises(ValueError, match="уже существует"):
        await service.create(code="drawing", name="Другой")

    repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_get_by_id_found(repo, service):
    """get_by_id возвращает домен, если найден."""
    dt = DocumentType(code="pz", name="Пояснительная записка")
    repo.get_by_id.return_value = dt

    result = await service.get_by_id(dt.id)

    assert result is dt
    repo.get_by_id.assert_called_once_with(dt.id)


@pytest.mark.asyncio
async def test_get_by_id_not_found(repo, service):
    """get_by_id возвращает None, если не найден."""
    repo.get_by_id.return_value = None

    result = await service.get_by_id(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_list_all(repo, service):
    """list_all возвращает список типов."""
    repo.list_all.return_value = [
        DocumentType(code="a", name="A"),
        DocumentType(code="b", name="B"),
    ]

    result = await service.list_all()

    assert len(result) == 2
    assert result[0].code == "a"
    assert result[1].code == "b"


# ---------- Обновление ----------


@pytest.mark.asyncio
async def test_update_name_and_gost_code(repo, service):
    """Обновление name и gost_code."""
    existing = DocumentType(code="drawing", name="Old")
    repo.get_by_id.return_value = existing
    repo.save.side_effect = lambda dt: dt

    result = await service.update(existing.id, name="New", gost_code="ГОСТ 123")

    assert result.name == "New"
    assert result.gost_code == "ГОСТ 123"
    assert result.code == "drawing"  # не изменилось
    repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_update_not_found(repo, service):
    """update возвращает None, если не найден."""
    repo.get_by_id.return_value = None

    result = await service.update(uuid4(), name="X")

    assert result is None
    repo.save.assert_not_called()


# ---------- Удаление ----------


@pytest.mark.asyncio
async def test_delete_success(repo, service):
    """Удаление типа проходит успешно.

    DocumentType НЕ имеет is_system — блокировки нет.
    """
    existing = DocumentType(code="custom", name="Custom")
    repo.get_by_id.return_value = existing

    result = await service.delete(existing.id)

    assert result is True
    repo.delete.assert_called_once_with(existing.id)


@pytest.mark.asyncio
async def test_delete_not_found(repo, service):
    """Удаление несуществующего типа → False."""
    repo.get_by_id.return_value = None

    result = await service.delete(uuid4())

    assert result is False
    repo.delete.assert_not_called()
