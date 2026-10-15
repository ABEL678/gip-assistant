"""Тесты DocumentVersionService."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from backend.src.domain.entities.document import Document
from backend.src.domain.entities.document_version import DocumentVersion
from backend.src.domain.services.document_version_service import DocumentVersionService


@pytest.fixture
def version_repo():
    return AsyncMock()


@pytest.fixture
def document_repo():
    return AsyncMock()


@pytest.fixture
def service(version_repo, document_repo):
    return DocumentVersionService(version_repo, document_repo)


@pytest.fixture
def document_id():
    return uuid4()


@pytest.fixture
def document(document_id):
    return Document(
        project_id=uuid4(),
        document_type_id=uuid4(),
        document_name="ПЗ",
        cipher="АБЗ-001-ПЗ",
    )


# ---------- Создание версии ----------


@pytest.mark.asyncio
async def test_create_minimal(version_repo, document_repo, service, document_id, document):
    """Создание версии с минимальным набором полей."""
    document_repo.get_by_id.return_value = document
    version_repo.save.side_effect = lambda v: v

    result = await service.create(
        document_id=document_id,
        version="v1.0",
        file_path="/files/v1.pdf",
        file_name="v1.pdf",
        hash_sha256="a" * 64,
        format_original="pdf",
        size_bytes=1024,
    )

    assert result.version == "v1.0"
    assert result.document_id == document_id
    assert result.hash_sha256 == "a" * 64
    assert result.size_bytes == 1024
    assert result.is_current is False
    assert result.change_number is None
    assert result.format_archive is None
    version_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_with_all_fields(version_repo, document_repo, service, document_id, document):
    """Создание версии со всеми полями."""
    document_repo.get_by_id.return_value = document
    version_repo.save.side_effect = lambda v: v

    uploaded_by = uuid4()
    result = await service.create(
        document_id=document_id,
        version="v1.1",
        file_path="/files/v1_1.pdf",
        file_name="v1_1.pdf",
        hash_sha256="b" * 64,
        format_original="pdf",
        size_bytes=2048,
        change_number=1,
        format_archive="zip",
        uploaded_by=uploaded_by,
    )

    assert result.version == "v1.1"
    assert result.change_number == 1
    assert result.format_archive == "zip"
    assert result.uploaded_by == uploaded_by
    assert result.size_bytes == 2048


@pytest.mark.asyncio
async def test_create_rejects_missing_document(version_repo, document_repo, service):
    """document_id не найден → ValueError."""
    document_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найден"):
        await service.create(
            document_id=uuid4(),
            version="v1.0",
            file_path="/f",
            file_name="f",
            hash_sha256="a" * 64,
            format_original="pdf",
            size_bytes=1,
        )

    version_repo.save.assert_not_called()


# ---------- Чтение ----------


@pytest.mark.asyncio
async def test_get_by_id_found(version_repo, service):
    """get_by_id возвращает версию, если найдена."""
    version = DocumentVersion(
        document_id=uuid4(),
        version="v1.0",
        file_path="/f",
        file_name="f",
        hash_sha256="a" * 64,
        format_original="pdf",
        size_bytes=1024,
    )
    version_repo.get_by_id.return_value = version

    result = await service.get_by_id(version.id)

    assert result is version
    version_repo.get_by_id.assert_called_once_with(version.id)


@pytest.mark.asyncio
async def test_get_by_id_not_found(version_repo, service):
    """get_by_id возвращает None, если не найдена."""
    version_repo.get_by_id.return_value = None

    result = await service.get_by_id(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_list_by_document(version_repo, service):
    """list_by_document возвращает список версий."""
    v1 = DocumentVersion(
        document_id=uuid4(), version="v1.0", file_path="/f1", file_name="f1",
        hash_sha256="a" * 64, format_original="pdf", size_bytes=1024,
    )
    v2 = DocumentVersion(
        document_id=v1.document_id, version="v1.1", file_path="/f2", file_name="f2",
        hash_sha256="b" * 64, format_original="pdf", size_bytes=2048,
    )
    version_repo.list_by_document.return_value = [v1, v2]

    result = await service.list_by_document(v1.document_id)

    assert len(result) == 2
    assert result[0].version == "v1.0"
    assert result[1].version == "v1.1"


@pytest.mark.asyncio
async def test_get_current_found(version_repo, service):
    """get_current возвращает версию, если is_current=True."""
    version = DocumentVersion(
        document_id=uuid4(),
        version="v1.0",
        file_path="/f",
        file_name="f",
        hash_sha256="a" * 64,
        format_original="pdf",
        size_bytes=1024,
        is_current=True,
    )
    version_repo.get_current.return_value = version

    result = await service.get_current(version.document_id)

    assert result is version


@pytest.mark.asyncio
async def test_get_current_not_found(version_repo, service):
    """get_current возвращает None, если нет текущей версии."""
    version_repo.get_current.return_value = None

    result = await service.get_current(uuid4())

    assert result is None


# ---------- set_current ----------


@pytest.mark.asyncio
async def test_set_current_success(version_repo, document_repo, service, document_id, document):
    """set_current работает при всех валидных данных."""
    document_repo.get_by_id.return_value = document
    version = DocumentVersion(
        document_id=document_id,
        version="v1.0",
        file_path="/f",
        file_name="f",
        hash_sha256="a" * 64,
        format_original="pdf",
        size_bytes=1024,
    )
    version_repo.get_by_id.return_value = version
    version_repo.set_current.return_value = None
    document_repo.save.side_effect = lambda d: d

    await service.set_current(document_id, version.id)

    version_repo.set_current.assert_called_once_with(document_id, version.id)
    document_repo.save.assert_called_once_with(document)
    assert document.current_version_id == version.id


@pytest.mark.asyncio
async def test_set_current_rejects_missing_document(version_repo, document_repo, service):
    """document_id не найден → ValueError."""
    document_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найден"):
        await service.set_current(uuid4(), uuid4())

    version_repo.set_current.assert_not_called()


@pytest.mark.asyncio
async def test_set_current_rejects_missing_version(version_repo, document_repo, service, document):
    """version_id не найден → ValueError."""
    document_repo.get_by_id.return_value = document
    version_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найдена"):
        await service.set_current(document.id, uuid4())

    version_repo.set_current.assert_not_called()


@pytest.mark.asyncio
async def test_set_current_rejects_mismatched_document(version_repo, document_repo, service, document_id, document):
    """version_id принадлежит другому документу → ValueError."""
    document_repo.get_by_id.return_value = document
    wrong_version = DocumentVersion(
        document_id=uuid4(),
        version="v1.0",
        file_path="/f",
        file_name="f",
        hash_sha256="a" * 64,
        format_original="pdf",
        size_bytes=1024,
    )
    version_repo.get_by_id.return_value = wrong_version

    with pytest.raises(ValueError, match="не принадлежит"):
        await service.set_current(document_id, wrong_version.id)

    version_repo.set_current.assert_not_called()


# ---------- Удаление ----------


@pytest.mark.asyncio
async def test_delete_non_current_version(version_repo, document_repo, service):
    """Удаление не-текущей версии — document.current_version_id не трогается."""
    version = DocumentVersion(
        document_id=uuid4(),
        version="v1.0",
        file_path="/f",
        file_name="f",
        hash_sha256="a" * 64,
        format_original="pdf",
        size_bytes=1024,
        is_current=False,
    )
    version_repo.get_by_id.return_value = version

    result = await service.delete(version.id)

    assert result is True
    version_repo.delete.assert_called_once_with(version.id)
    document_repo.save.assert_not_called()
    document_repo.get_by_id.assert_not_called()


@pytest.mark.asyncio
async def test_delete_current_version_resets_document(version_repo, document_repo, service, document):
    """Удаление текущей версии — сбрасывает document.current_version_id."""
    version = DocumentVersion(
        document_id=document.id,
        version="v1.0",
        file_path="/f",
        file_name="f",
        hash_sha256="a" * 64,
        format_original="pdf",
        size_bytes=1024,
        is_current=True,
    )
    version_repo.get_by_id.return_value = version
    document_repo.get_by_id.return_value = document
    document_repo.save.side_effect = lambda d: d

    result = await service.delete(version.id)

    assert result is True
    version_repo.delete.assert_called_once_with(version.id)
    document_repo.save.assert_called_once_with(document)
    assert document.current_version_id is None


@pytest.mark.asyncio
async def test_delete_not_found(version_repo, service):
    """Удаление несуществующей версии → False."""
    version_repo.get_by_id.return_value = None

    result = await service.delete(uuid4())

    assert result is False
    version_repo.delete.assert_not_called()
