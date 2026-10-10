"""Тесты EntityTypeService."""

from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from backend.src.domain.entities.entity_type import EntityType
from backend.src.domain.services.entity_type_service import EntityTypeService


@pytest.fixture
def repo():
    return AsyncMock()


@pytest.fixture
def project_id() -> UUID:
    return uuid4()


@pytest.fixture
def service(repo):
    return EntityTypeService(repo)


# ---------- Успешные сценарии ----------


@pytest.mark.asyncio
async def test_create_minimal(repo, service, project_id):
    """Создание типа с минимальным набором полей."""
    repo.save.side_effect = lambda et: et

    result = await service.create(project_id=project_id, name="Исходные данные")

    assert result.name == "Исходные данные"
    assert result.icon == "📄"
    assert result.color == "gray"
    assert result.field_schema == {"fields": []}
    assert result.project_id == project_id
    repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_with_schema(repo, service, project_id):
    """Создание типа с полной схемой полей."""
    repo.save.side_effect = lambda et: et
    schema = {
        "fields": [
            {"key": "title", "label": "Наименование", "type": "text", "required": True},
            {"key": "status", "label": "Статус", "type": "select", "options": ["Да", "Нет"]},
        ]
    }

    result = await service.create(
        project_id=project_id,
        name="ИД",
        icon="📋",
        color="blue",
        description="Исходные данные",
        field_schema=schema,
        sort_order=5,
    )

    assert result.icon == "📋"
    assert result.color == "blue"
    assert result.description == "Исходные данные"
    assert result.sort_order == 5
    assert result.field_schema == schema


@pytest.mark.asyncio
async def test_create_rejects_duplicate_field_keys(repo, service, project_id):
    """Дублирующиеся key в схеме → ValueError."""
    schema = {
        "fields": [
            {"key": "title", "label": "A", "type": "text"},
            {"key": "title", "label": "B", "type": "text"},
        ]
    }

    with pytest.raises(ValueError, match="уникальны"):
        await service.create(
            project_id=project_id,
            name="Тип",
            field_schema=schema,
        )
    repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_get_by_id_found(repo, service):
    """get_by_id возвращает домен, если найден."""
    entity_type = EntityType(project_id=uuid4(), name="Test")
    repo.get_by_id.return_value = entity_type

    result = await service.get_by_id(entity_type.id)

    assert result is entity_type
    repo.get_by_id.assert_called_once_with(entity_type.id)


@pytest.mark.asyncio
async def test_get_by_id_not_found(repo, service):
    """get_by_id возвращает None, если не найден."""
    repo.get_by_id.return_value = None

    result = await service.get_by_id(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_list_by_project(repo, service, project_id):
    """list_by_project возвращает список типов."""
    repo.list_by_project.return_value = [
        EntityType(project_id=project_id, name="A"),
        EntityType(project_id=project_id, name="B"),
    ]

    result = await service.list_by_project(project_id)

    assert len(result) == 2
    assert result[0].name == "A"
    assert result[1].name == "B"


# ---------- Обновление ----------


@pytest.mark.asyncio
async def test_update_name_only(repo, service):
    """Обновление только name."""
    existing = EntityType(project_id=uuid4(), name="Old")
    repo.get_by_id.return_value = existing
    repo.save.side_effect = lambda et: et

    result = await service.update(existing.id, name="New")

    assert result is not None
    assert result.name == "New"
    assert result.icon == "📄"  # не изменилось


@pytest.mark.asyncio
async def test_update_full(repo, service):
    """Обновление всех полей."""
    existing = EntityType(project_id=uuid4(), name="Old")
    repo.get_by_id.return_value = existing
    repo.save.side_effect = lambda et: et
    new_schema = {"fields": [{"key": "a", "label": "A", "type": "text"}]}

    result = await service.update(
        existing.id,
        name="New",
        icon="🔥",
        color="red",
        description="desc",
        field_schema=new_schema,
        sort_order=99,
    )

    assert result is not None
    assert result.name == "New"
    assert result.icon == "🔥"
    assert result.color == "red"
    assert result.description == "desc"
    assert result.field_schema == new_schema
    assert result.sort_order == 99


@pytest.mark.asyncio
async def test_update_not_found(repo, service):
    """update возвращает None, если тип не найден."""
    repo.get_by_id.return_value = None

    result = await service.update(uuid4(), name="X")

    assert result is None
    repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_update_rejects_invalid_schema(repo, service):
    """Обновление schema с дублями → ValueError."""
    existing = EntityType(project_id=uuid4(), name="Old")
    repo.get_by_id.return_value = existing

    bad_schema = {
        "fields": [
            {"key": "x", "label": "A", "type": "text"},
            {"key": "x", "label": "B", "type": "text"},
        ]
    }

    with pytest.raises(ValueError, match="уникальны"):
        await service.update(existing.id, field_schema=bad_schema)


# ---------- Удаление ----------


@pytest.mark.asyncio
async def test_delete_success(repo, service):
    """Удаление пользовательского типа проходит успешно."""
    existing = EntityType(project_id=uuid4(), name="Custom", is_system=False)
    repo.get_by_id.return_value = existing

    result = await service.delete(existing.id)

    assert result is True
    repo.delete.assert_called_once_with(existing.id)


@pytest.mark.asyncio
async def test_delete_system_type_forbidden(repo, service):
    """Системный тип удалить нельзя."""
    existing = EntityType(project_id=uuid4(), name="Sys", is_system=True)
    repo.get_by_id.return_value = existing

    with pytest.raises(ValueError, match="системный"):
        await service.delete(existing.id)

    repo.delete.assert_not_called()


@pytest.mark.asyncio
async def test_delete_not_found(repo, service):
    """Удаление несуществующего типа → False."""
    repo.get_by_id.return_value = None

    result = await service.delete(uuid4())

    assert result is False
    repo.delete.assert_not_called()