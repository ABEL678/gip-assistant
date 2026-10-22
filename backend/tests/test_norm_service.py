"""Тесты NormService."""

from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from backend.src.domain.entities.norm import Norm
from backend.src.domain.services.norm_service import NormService
from backend.src.domain.value_objects.enums import NormType


@pytest.fixture
def mock_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.get_by_code = AsyncMock()
    repo.list_by_project = AsyncMock()
    repo.save = AsyncMock()
    repo.delete = AsyncMock()
    return repo


@pytest.fixture
def service(mock_repo: AsyncMock) -> NormService:
    return NormService(mock_repo)


@pytest.fixture
def project_id() -> UUID:
    return uuid4()


@pytest.fixture
def valid_norm(project_id: UUID) -> Norm:
    return Norm(
        id=uuid4(),
        project_id=project_id,
        code="ГОСТ Р 21.101-2026",
        title="Основные положения",
        norm_type=NormType.GOST,
    )


# ---------- Чтение ----------


@pytest.mark.asyncio
async def test_get_found(
    service: NormService, mock_repo: AsyncMock, valid_norm: Norm,
):
    """get — находит норму по ID."""
    mock_repo.get_by_id.return_value = valid_norm

    result = await service.get(valid_norm.id)

    assert result is valid_norm


@pytest.mark.asyncio
async def test_get_not_found(service: NormService, mock_repo: AsyncMock):
    """get — возвращает None если не найдена."""
    mock_repo.get_by_id.return_value = None

    result = await service.get(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_list_by_project(
    service: NormService, mock_repo: AsyncMock, valid_norm: Norm,
):
    """list_by_project — возвращает список норм."""
    mock_repo.list_by_project.return_value = [valid_norm]

    result = await service.list_by_project(valid_norm.project_id)

    assert len(result) == 1
    assert result[0].id == valid_norm.id


# ---------- Создание ----------


@pytest.mark.asyncio
async def test_create_success(
    service: NormService, mock_repo: AsyncMock, project_id: UUID,
):
    """create — создаёт норму при успешной валидации."""
    mock_repo.get_by_code.return_value = None
    mock_repo.save.side_effect = lambda n: n

    result = await service.create(
        project_id=project_id,
        code="ГОСТ Р 21.101-2026",
        title="Основные положения по проектированию",
        norm_type=NormType.GOST,
    )

    assert result.code == "ГОСТ Р 21.101-2026"
    assert result.norm_type == NormType.GOST
    mock_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_empty_code(service: NormService, mock_repo: AsyncMock):
    """create — пустое обозначение → ValueError."""
    with pytest.raises(ValueError, match="Обозначение .* не может быть пустым"):
        await service.create(
            project_id=uuid4(),
            code="   ",
            title="Название",
            norm_type=NormType.GOST,
        )

    mock_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_empty_title(service: NormService, mock_repo: AsyncMock):
    """create — пустое название → ValueError."""
    with pytest.raises(ValueError, match="Название .* не может быть пустым"):
        await service.create(
            project_id=uuid4(),
            code="ГОСТ 1.0",
            title="   ",
            norm_type=NormType.GOST,
        )

    mock_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_duplicate_code(
    service: NormService, mock_repo: AsyncMock, valid_norm: Norm,
):
    """create — обозначение уже занято в проекте → ValueError."""
    mock_repo.get_by_code.return_value = valid_norm

    with pytest.raises(ValueError, match="уже существует в проекте"):
        await service.create(
            project_id=valid_norm.project_id,
            code=valid_norm.code,
            title="Другое название",
            norm_type=NormType.SNIP,
        )

    mock_repo.save.assert_not_called()


# ---------- Обновление ----------


@pytest.mark.asyncio
async def test_update_success(
    service: NormService, mock_repo: AsyncMock, valid_norm: Norm,
):
    """update — обновляет название нормы."""
    mock_repo.get_by_id.return_value = valid_norm
    mock_repo.save.side_effect = lambda n: n

    result = await service.update(valid_norm.id, title="Новое название")

    assert result.title == "Новое название"
    mock_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_update_keeps_own_code(
    service: NormService, mock_repo: AsyncMock, valid_norm: Norm,
):
    """update — сохранение своего же code не считается дубликатом."""
    mock_repo.get_by_id.return_value = valid_norm
    mock_repo.get_by_code.return_value = valid_norm
    mock_repo.save.side_effect = lambda n: n

    result = await service.update(valid_norm.id, code=valid_norm.code)

    assert result.code == valid_norm.code
    mock_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_update_duplicate_code(
    service: NormService, mock_repo: AsyncMock, valid_norm: Norm,
):
    """update — code занят другой нормой проекта → ValueError."""
    other_norm = Norm(
        id=uuid4(),
        project_id=valid_norm.project_id,
        code="СНиП 1.0",
        title="Другая норма",
        norm_type=NormType.SNIP,
    )
    mock_repo.get_by_id.return_value = other_norm
    mock_repo.get_by_code.return_value = valid_norm

    with pytest.raises(ValueError, match="уже существует в проекте"):
        await service.update(other_norm.id, code=valid_norm.code)

    mock_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_update_not_found(service: NormService, mock_repo: AsyncMock):
    """update — норма не найдена → ValueError."""
    mock_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найдена"):
        await service.update(uuid4(), title="Новое")

    mock_repo.save.assert_not_called()


# ---------- Удаление ----------


@pytest.mark.asyncio
async def test_delete_success(
    service: NormService, mock_repo: AsyncMock, valid_norm: Norm,
):
    """delete — удаляет найденную норму."""
    mock_repo.get_by_id.return_value = valid_norm

    await service.delete(valid_norm.id)

    mock_repo.delete.assert_called_once_with(valid_norm.id)


@pytest.mark.asyncio
async def test_delete_not_found(service: NormService, mock_repo: AsyncMock):
    """delete — норма не найдена → ValueError."""
    mock_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найдена"):
        await service.delete(uuid4())

    mock_repo.delete.assert_not_called()
