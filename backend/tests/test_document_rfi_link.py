"""DocumentService — валидация rfi_id (spec_week_4.md §2.2)."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from backend.src.domain.services.document_service import DocumentService


@pytest.fixture
def document_repo():
    repo = AsyncMock()
    repo.save.side_effect = lambda d: d
    return repo


@pytest.fixture
def document_type_repo():
    repo = AsyncMock()
    return repo


@pytest.fixture
def task_repo():
    repo = AsyncMock()
    return repo


@pytest.fixture
def service(document_repo, document_type_repo, task_repo):
    return DocumentService(
        repo=document_repo,
        document_type_repo=document_type_repo,
        task_repo=task_repo,
    )


@pytest.mark.asyncio
async def test_create_document_rfi_id_non_rfi_task(service, task_repo):
    """rfi_id на не-RFI Task → ValueError."""
    task_id = uuid4()
    task_repo.get_by_id.return_value = AsyncMock(
        is_rfi=False, project_id=uuid4()
    )

    with pytest.raises(ValueError, match="не является RFI"):
        await service.create(
            project_id=uuid4(),
            document_type_id=uuid4(),
            document_name="Test",
            cipher="TEST-001",
            rfi_id=task_id,
        )


@pytest.mark.asyncio
async def test_create_document_rfi_id_wrong_project(service, task_repo):
    """rfi_id на RFI из другого проекта → ValueError."""
    task_id = uuid4()
    other_project = uuid4()
    task_repo.get_by_id.return_value = AsyncMock(
        is_rfi=True, project_id=other_project
    )

    with pytest.raises(ValueError, match="другому проекту"):
        await service.create(
            project_id=uuid4(),
            document_type_id=uuid4(),
            document_name="Test",
            cipher="TEST-001",
            rfi_id=task_id,
        )


@pytest.mark.asyncio
async def test_update_document_rfi_id_non_rfi_task(service, document_repo, task_repo):
    """update: rfi_id на не-RFI Task → ValueError."""
    doc_id = uuid4()
    task_id = uuid4()
    document = AsyncMock(
        id=doc_id,
        project_id=uuid4(),
    )
    document_repo.get_by_id.return_value = document
    task_repo.get_by_id.return_value = AsyncMock(
        is_rfi=False, project_id=uuid4()
    )

    with pytest.raises(ValueError, match="не является RFI"):
        await service.update(doc_id, rfi_id=task_id)


@pytest.mark.asyncio
async def test_update_document_rfi_id_wrong_project(service, document_repo, task_repo):
    """update: rfi_id на RFI из другого проекта → ValueError."""
    doc_id = uuid4()
    task_id = uuid4()
    document = AsyncMock(
        id=doc_id,
        project_id=uuid4(),
    )
    document_repo.get_by_id.return_value = document
    other_project = uuid4()
    task_repo.get_by_id.return_value = AsyncMock(
        is_rfi=True, project_id=other_project
    )

    with pytest.raises(ValueError, match="другому проекту"):
        await service.update(doc_id, rfi_id=task_id)


@pytest.mark.asyncio
async def test_create_document_no_rfi_id(service, document_repo, document_type_repo):
    """Без rfi_id — работает."""
    document_type_repo.get_by_id.return_value = AsyncMock()

    result = await service.create(
        project_id=uuid4(),
        document_type_id=uuid4(),
        document_name="Test",
        cipher="TEST-001",
    )

    assert result is not None
    document_repo.save.assert_called_once()
