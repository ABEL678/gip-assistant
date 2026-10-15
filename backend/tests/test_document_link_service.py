"""Тесты DocumentLinkService."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from backend.src.domain.entities.document import Document
from backend.src.domain.entities.document_link import DocumentLink
from backend.src.domain.services.document_link_service import DocumentLinkService
from backend.src.domain.value_objects.document import DocumentLinkType


@pytest.fixture
def repo():
    return AsyncMock()


@pytest.fixture
def document_repo():
    return AsyncMock()


@pytest.fixture
def service(repo, document_repo):
    return DocumentLinkService(repo, document_repo)


@pytest.fixture
def project_id():
    return uuid4()


@pytest.fixture
def source_doc(project_id):
    return Document(
        project_id=project_id,
        document_type_id=uuid4(),
        document_name="Source",
        cipher="S",
    )


@pytest.fixture
def target_doc(project_id):
    return Document(
        project_id=project_id,
        document_type_id=uuid4(),
        document_name="Target",
        cipher="T",
    )


# ---------- Создание связи ----------


@pytest.mark.asyncio
async def test_create_success(repo, document_repo, service, source_doc, target_doc):
    """Создание связи с валидными данными."""
    def get_doc(id):
        if id == source_doc.id:
            return source_doc
        if id == target_doc.id:
            return target_doc
        return None

    document_repo.get_by_id.side_effect = get_doc
    repo.save.side_effect = lambda link: link

    result = await service.create(source_doc.id, target_doc.id, DocumentLinkType.APPENDIX)

    assert result.source_document_id == source_doc.id
    assert result.target_document_id == target_doc.id
    assert result.link_type == DocumentLinkType.APPENDIX
    repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_rejects_self_link(repo, document_repo, service, source_doc):
    """source == target → ValueError."""
    with pytest.raises(ValueError, match="сам с собой"):
        await service.create(source_doc.id, source_doc.id, DocumentLinkType.REFERENCE)

    repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_rejects_missing_source(repo, document_repo, service):
    """source не найден → ValueError."""
    document_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найден"):
        await service.create(uuid4(), uuid4(), DocumentLinkType.APPENDIX)

    repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_rejects_missing_target(repo, document_repo, service, source_doc):
    """target не найден → ValueError."""
    document_repo.get_by_id.side_effect = lambda id: source_doc if id == source_doc.id else None

    with pytest.raises(ValueError, match="не найден"):
        await service.create(source_doc.id, uuid4(), DocumentLinkType.APPENDIX)

    repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_rejects_different_projects(repo, document_repo, service, source_doc):
    """Документы из разных проектов → ValueError."""
    target_other = Document(
        project_id=uuid4(),
        document_type_id=uuid4(),
        document_name="Other",
        cipher="O",
    )
    document_repo.get_by_id.side_effect = lambda id: source_doc if id == source_doc.id else target_other

    with pytest.raises(ValueError, match="разных проектов"):
        await service.create(source_doc.id, target_other.id, DocumentLinkType.APPENDIX)

    repo.save.assert_not_called()


# ---------- Чтение ----------


@pytest.mark.asyncio
async def test_get_by_id_found(repo, service):
    """get_by_id возвращает связь, если найдена."""
    link = DocumentLink(
        source_document_id=uuid4(),
        target_document_id=uuid4(),
        link_type=DocumentLinkType.APPENDIX,
    )
    repo.get_by_id.return_value = link

    result = await service.get_by_id(link.id)

    assert result is link
    repo.get_by_id.assert_called_once_with(link.id)


@pytest.mark.asyncio
async def test_get_by_id_not_found(repo, service):
    """get_by_id возвращает None, если не найдена."""
    repo.get_by_id.return_value = None

    result = await service.get_by_id(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_list_by_source(repo, service, source_doc):
    """list_by_source возвращает связи, где source_doc — источник."""
    link1 = DocumentLink(
        source_document_id=source_doc.id,
        target_document_id=uuid4(),
        link_type=DocumentLinkType.APPENDIX,
    )
    link2 = DocumentLink(
        source_document_id=source_doc.id,
        target_document_id=uuid4(),
        link_type=DocumentLinkType.REFERENCE,
    )
    repo.list_by_source.return_value = [link1, link2]

    result = await service.list_by_source(source_doc.id)

    assert len(result) == 2
    assert result[0].link_type == DocumentLinkType.APPENDIX
    assert result[1].link_type == DocumentLinkType.REFERENCE


@pytest.mark.asyncio
async def test_list_by_target(repo, service, target_doc):
    """list_by_target возвращает связи, где target_doc — цель."""
    link = DocumentLink(
        source_document_id=uuid4(),
        target_document_id=target_doc.id,
        link_type=DocumentLinkType.APPENDIX,
    )
    repo.list_by_target.return_value = [link]

    result = await service.list_by_target(target_doc.id)

    assert len(result) == 1
    assert result[0].target_document_id == target_doc.id


# ---------- Удаление ----------


@pytest.mark.asyncio
async def test_delete_success(repo, service):
    """Удаление связи проходит успешно."""
    link = DocumentLink(
        source_document_id=uuid4(),
        target_document_id=uuid4(),
        link_type=DocumentLinkType.APPENDIX,
    )
    repo.get_by_id.return_value = link

    result = await service.delete(link.id)

    assert result is True
    repo.delete.assert_called_once_with(link.id)


@pytest.mark.asyncio
async def test_delete_not_found(repo, service):
    """Удаление несуществующей связи → False."""
    repo.get_by_id.return_value = None

    result = await service.delete(uuid4())

    assert result is False
    repo.delete.assert_not_called()
