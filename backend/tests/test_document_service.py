"""Тесты DocumentService."""

from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from backend.src.domain.entities.document import Document
from backend.src.domain.entities.document_type import DocumentType
from backend.src.domain.services.document_service import DocumentService
from backend.src.domain.value_objects.document import (
    DocPartType,
    DocumentKind,
    LifecycleStatus,
)


@pytest.fixture
def repo():
    return AsyncMock()


@pytest.fixture
def document_type_repo():
    return AsyncMock()


@pytest.fixture
def project_id() -> UUID:
    return uuid4()


@pytest.fixture
def document_type(project_id) -> DocumentType:
    return DocumentType(code="pz", name="Пояснительная записка")


@pytest.fixture
def service(repo, document_type_repo):
    return DocumentService(
        repo, document_type_repo, task_repo=AsyncMock()
    )


# ---------- Создание ----------


@pytest.mark.asyncio
async def test_create_minimal(repo, document_type_repo, service, project_id, document_type):
    """Создание документа с минимальным набором полей."""
    document_type_repo.get_by_id.return_value = document_type
    repo.save.side_effect = lambda d: d

    result = await service.create(
        project_id=project_id,
        document_type_id=document_type.id,
        document_name="ПЗ",
        cipher="АБЗ-001-ПЗ",
    )

    assert result.document_name == "ПЗ"
    assert result.cipher == "АБЗ-001-ПЗ"
    assert result.document_kind == DocumentKind.PD
    assert result.lifecycle_status == LifecycleStatus.DRAFT
    assert result.project_id == project_id
    assert result.document_type_id == document_type.id
    assert isinstance(result.guid, UUID)
    assert result.guid is not None
    repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_with_all_fields(repo, document_type_repo, service, project_id, document_type):
    """Создание документа со всеми полями."""
    document_type_repo.get_by_id.return_value = document_type
    repo.save.side_effect = lambda d: d

    result = await service.create(
        project_id=project_id,
        document_type_id=document_type.id,
        document_name="ПЗ",
        cipher="АБЗ-001-ПЗ",
        document_kind=DocumentKind.RD,
        doc_part_type=DocPartType.TCH,
        section_code="АР",
        mark="АР",
        base_designation="АБЗГ.123456.789-24",
        lifecycle_status=LifecycleStatus.IN_REVIEW,
    )

    assert result.document_name == "ПЗ"
    assert result.cipher == "АБЗ-001-ПЗ"
    assert result.document_kind == DocumentKind.RD
    assert result.doc_part_type == DocPartType.TCH
    assert result.section_code == "АР"
    assert result.mark == "АР"
    assert result.base_designation == "АБЗГ.123456.789-24"
    assert result.lifecycle_status == LifecycleStatus.IN_REVIEW
    assert result.project_id == project_id


@pytest.mark.asyncio
async def test_create_rejects_missing_document_type(repo, document_type_repo, service, project_id):
    """document_type_id не найден → ValueError."""
    document_type_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найден"):
        await service.create(
            project_id=project_id,
            document_type_id=uuid4(),
            document_name="X",
            cipher="Y",
        )

    repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_get_by_id_found(repo, service):
    """get_by_id возвращает домен, если найден."""
    doc = Document(
        project_id=uuid4(),
        document_type_id=uuid4(),
        document_name="ПЗ",
        cipher="X",
    )
    repo.get_by_id.return_value = doc

    result = await service.get_by_id(doc.id)

    assert result is doc
    repo.get_by_id.assert_called_once_with(doc.id)


@pytest.mark.asyncio
async def test_get_by_id_not_found(repo, service):
    """get_by_id возвращает None."""
    repo.get_by_id.return_value = None

    result = await service.get_by_id(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_get_by_guid_found(repo, service):
    """get_by_guid возвращает домен, если найден."""
    doc = Document(
        project_id=uuid4(),
        document_type_id=uuid4(),
        document_name="ПЗ",
        cipher="X",
    )
    repo.get_by_guid.return_value = doc

    result = await service.get_by_guid(doc.guid)

    assert result is doc
    repo.get_by_guid.assert_called_once_with(doc.guid)


@pytest.mark.asyncio
async def test_get_by_guid_not_found(repo, service):
    """get_by_guid возвращает None."""
    repo.get_by_guid.return_value = None

    result = await service.get_by_guid(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_list_by_project(repo, service, project_id):
    """list_by_project возвращает список документов."""
    doc1 = Document(project_id=project_id, document_type_id=uuid4(), document_name="A", cipher="1")
    doc2 = Document(project_id=project_id, document_type_id=uuid4(), document_name="B", cipher="2")
    repo.list_by_project.return_value = [doc1, doc2]

    result = await service.list_by_project(project_id)

    assert len(result) == 2
    assert result[0].document_name == "A"
    assert result[1].document_name == "B"


@pytest.mark.asyncio
async def test_list_by_project_with_status_filter(repo, service, project_id):
    """list_by_project с фильтром статуса."""
    doc = Document(project_id=project_id, document_type_id=uuid4(), document_name="X", cipher="Y")
    repo.list_by_project.return_value = [doc]

    await service.list_by_project(project_id, lifecycle_status=LifecycleStatus.DRAFT)

    repo.list_by_project.assert_called_once_with(
        project_id, lifecycle_status=LifecycleStatus.DRAFT
    )


# ---------- Обновление ----------


@pytest.mark.asyncio
async def test_update_document_name(repo, service, project_id, document_type):
    """Обновление только document_name."""
    existing = Document(
        project_id=project_id,
        document_type_id=document_type.id,
        document_name="Old",
        cipher="X",
    )
    repo.get_by_id.return_value = existing
    repo.save.side_effect = lambda d: d

    result = await service.update(existing.id, document_name="New")

    assert result.document_name == "New"
    assert result.cipher == "X"  # не изменилось
    repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_update_not_found(repo, service):
    """update возвращает None, если не найден."""
    repo.get_by_id.return_value = None

    result = await service.update(uuid4(), document_name="X")

    assert result is None
    repo.save.assert_not_called()


# ---------- Удаление ----------


@pytest.mark.asyncio
async def test_delete_success(repo, service, project_id, document_type):
    """Удаление документа проходит успешно."""
    existing = Document(
        project_id=project_id,
        document_type_id=document_type.id,
        document_name="X",
        cipher="Y",
    )
    repo.get_by_id.return_value = existing

    result = await service.delete(existing.id)

    assert result is True
    repo.delete.assert_called_once_with(existing.id)


@pytest.mark.asyncio
async def test_delete_not_found(repo, service):
    """Удаление несуществующего документа → False."""
    repo.get_by_id.return_value = None

    result = await service.delete(uuid4())

    assert result is False
    repo.delete.assert_not_called()
