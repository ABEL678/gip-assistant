"""Тесты EntityService."""

from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from backend.src.domain.entities.entity import Entity
from backend.src.domain.entities.entity_type import EntityType
from backend.src.domain.services.entity_service import EntityService


@pytest.fixture
def repo():
    return AsyncMock()


@pytest.fixture
def entity_type_repo():
    return AsyncMock()


@pytest.fixture
def project_id() -> UUID:
    return uuid4()


@pytest.fixture
def entity_type(project_id) -> EntityType:
    """Тип с обязательным полем title."""
    return EntityType(
        id=uuid4(),
        project_id=project_id,
        name="Исходные данные",
        field_schema={
            "fields": [
                {"key": "title", "label": "Наименование", "type": "text", "required": True},
                {"key": "status", "label": "Статус", "type": "select", "options": ["Да", "Нет"]},
            ]
        },
    )


@pytest.fixture
def service(repo, entity_type_repo):
    return EntityService(repo, entity_type_repo)


# ---------- Успешные сценарии ----------


@pytest.mark.asyncio
async def test_create_minimal(repo, entity_type_repo, service, project_id, entity_type):
    """Создание записи с обязательным полем."""
    entity_type_repo.get_by_id.return_value = entity_type
    repo.save.side_effect = lambda e: e

    result = await service.create(
        project_id=project_id,
        entity_type_id=entity_type.id,
        data={"title": "ТУ на водоснабжение"},
    )

    assert result.data == {"title": "ТУ на водоснабжение"}
    assert result.project_id == project_id
    assert result.entity_type_id == entity_type.id
    repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_with_all_fields(repo, entity_type_repo, service, project_id, entity_type):
    """Создание с обязательным и необязательным полем."""
    entity_type_repo.get_by_id.return_value = entity_type
    repo.save.side_effect = lambda e: e

    result = await service.create(
        project_id=project_id,
        entity_type_id=entity_type.id,
        data={"title": "ТУ", "status": "Да"},
        sort_order=7,
    )

    assert result.data == {"title": "ТУ", "status": "Да"}
    assert result.sort_order == 7


@pytest.mark.asyncio
async def test_create_rejects_missing_required(repo, entity_type_repo, service, project_id, entity_type):
    """Отсутствует обязательное поле → ValueError."""
    entity_type_repo.get_by_id.return_value = entity_type

    with pytest.raises(ValueError, match="Наименование"):
        await service.create(
            project_id=project_id,
            entity_type_id=entity_type.id,
            data={"status": "Да"},  # нет title
        )
    repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_rejects_missing_entity_type(repo, entity_type_repo, service, project_id):
    """Тип сущности не найден → ValueError."""
    entity_type_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найден"):
        await service.create(
            project_id=project_id,
            entity_type_id=uuid4(),
            data={"title": "X"},
        )
    repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_rejects_mismatched_project(repo, entity_type_repo, service, entity_type):
    """project_id не совпадает с типом → ValueError."""
    entity_type_repo.get_by_id.return_value = entity_type
    wrong_project = uuid4()

    with pytest.raises(ValueError, match="другому проекту"):
        await service.create(
            project_id=wrong_project,
            entity_type_id=entity_type.id,
            data={"title": "X"},
        )
    repo.save.assert_not_called()


# ---------- Чтение ----------


@pytest.mark.asyncio
async def test_get_by_id_found(repo, service):
    """get_by_id возвращает запись, если найдена."""
    entity = Entity(project_id=uuid4(), entity_type_id=uuid4())
    repo.get_by_id.return_value = entity

    result = await service.get_by_id(entity.id)

    assert result is entity


@pytest.mark.asyncio
async def test_get_by_id_not_found(repo, service):
    """get_by_id возвращает None."""
    repo.get_by_id.return_value = None

    result = await service.get_by_id(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_list_by_type(repo, service):
    """list_by_type возвращает список записей."""
    type_id = uuid4()
    repo.list_by_type.return_value = [
        Entity(project_id=uuid4(), entity_type_id=type_id),
        Entity(project_id=uuid4(), entity_type_id=type_id),
    ]

    result = await service.list_by_type(type_id)

    assert len(result) == 2


# ---------- Обновление ----------


@pytest.mark.asyncio
async def test_update_data_only(repo, entity_type_repo, service, entity_type):
    """Обновление только data."""
    entity = Entity(
        project_id=entity_type.project_id,
        entity_type_id=entity_type.id,
        data={"title": "Старое"},
    )
    repo.get_by_id.return_value = entity
    entity_type_repo.get_by_id.return_value = entity_type
    repo.save.side_effect = lambda e: e

    result = await service.update(entity.id, data={"title": "Новое"})

    assert result is not None
    assert result.data == {"title": "Новое"}


@pytest.mark.asyncio
async def test_update_not_found(repo, service):
    """update возвращает None, если записи нет."""
    repo.get_by_id.return_value = None

    result = await service.update(uuid4(), data={"title": "X"})

    assert result is None
    repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_update_rejects_invalid_data(repo, entity_type_repo, service, entity_type):
    """Обновление data без обязательного поля → ValueError."""
    entity = Entity(
        project_id=entity_type.project_id,
        entity_type_id=entity_type.id,
        data={"title": "Старое"},
    )
    repo.get_by_id.return_value = entity
    entity_type_repo.get_by_id.return_value = entity_type

    with pytest.raises(ValueError, match="Наименование"):
        await service.update(entity.id, data={"status": "Да"})  # нет title


# ---------- Удаление ----------


@pytest.mark.asyncio
async def test_delete_success(repo, service):
    """Удаление записи проходит успешно."""
    entity = Entity(project_id=uuid4(), entity_type_id=uuid4())
    repo.get_by_id.return_value = entity

    result = await service.delete(entity.id)

    assert result is True
    repo.delete.assert_called_once_with(entity.id)


@pytest.mark.asyncio
async def test_delete_not_found(repo, service):
    """Удаление несуществующей записи → False."""
    repo.get_by_id.return_value = None

    result = await service.delete(uuid4())

    assert result is False
    repo.delete.assert_not_called()