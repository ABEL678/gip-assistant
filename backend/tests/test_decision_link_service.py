"""Тесты DecisionLinkService."""

from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from backend.src.domain.entities.decision import Decision
from backend.src.domain.entities.decision_link import DecisionLink
from backend.src.domain.services.decision_link_service import DecisionLinkService
from backend.src.domain.value_objects.enums import DecisionLinkType


@pytest.fixture
def mock_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.list_by_decision = AsyncMock()
    repo.list_by_project = AsyncMock()
    repo.save = AsyncMock()
    repo.delete = AsyncMock()
    return repo


@pytest.fixture
def mock_decision_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    return repo


@pytest.fixture
def service(mock_repo: AsyncMock, mock_decision_repo: AsyncMock) -> DecisionLinkService:
    return DecisionLinkService(mock_repo, mock_decision_repo)


@pytest.fixture
def project_id() -> UUID:
    return uuid4()


@pytest.fixture
def from_decision(project_id: UUID) -> Decision:
    return Decision(project_id=project_id, formulation="Решение 1")


@pytest.fixture
def to_decision(project_id: UUID) -> Decision:
    return Decision(project_id=project_id, formulation="Решение 2")


# ---------- Создание связи ----------


@pytest.mark.asyncio
async def test_create_success(
    service: DecisionLinkService,
    mock_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    project_id: UUID,
    from_decision: Decision,
    to_decision: Decision,
):
    """Создание связи с валидными данными."""
    def get_decision(id):
        if id == from_decision.id:
            return from_decision
        if id == to_decision.id:
            return to_decision
        return None

    mock_decision_repo.get_by_id.side_effect = get_decision
    mock_repo.list_by_project.return_value = []
    mock_repo.save.side_effect = lambda link: link

    result = await service.create(
        project_id,
        from_decision.id,
        to_decision.id,
        DecisionLinkType.SEQUENTIAL,
    )

    assert result.from_decision_id == from_decision.id
    assert result.to_decision_id == to_decision.id
    assert result.link_type == DecisionLinkType.SEQUENTIAL
    mock_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_rejects_self_link(
    service: DecisionLinkService,
    mock_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    project_id: UUID,
    from_decision: Decision,
):
    """from == to → ValueError (проверка до обращения к репозиториям)."""
    with pytest.raises(ValueError, match="само с собой"):
        await service.create(
            project_id,
            from_decision.id,
            from_decision.id,
            DecisionLinkType.SEQUENTIAL,
        )

    mock_decision_repo.get_by_id.assert_not_called()
    mock_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_rejects_missing_from(
    service: DecisionLinkService,
    mock_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    project_id: UUID,
):
    """from не найдено → ValueError."""
    mock_decision_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найдено"):
        await service.create(
            project_id, uuid4(), uuid4(), DecisionLinkType.SEQUENTIAL,
        )

    mock_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_rejects_missing_to(
    service: DecisionLinkService,
    mock_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    project_id: UUID,
    from_decision: Decision,
):
    """to не найдено → ValueError."""
    mock_decision_repo.get_by_id.side_effect = [from_decision, None]

    with pytest.raises(ValueError, match="не найдено"):
        await service.create(
            project_id, from_decision.id, uuid4(), DecisionLinkType.SEQUENTIAL,
        )

    mock_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_rejects_different_projects(
    service: DecisionLinkService,
    mock_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    project_id: UUID,
    from_decision: Decision,
):
    """Решения из разных проектов → ValueError."""
    other_decision = Decision(project_id=uuid4(), formulation="Чужое решение")

    def get_decision(id):
        if id == from_decision.id:
            return from_decision
        return other_decision

    mock_decision_repo.get_by_id.side_effect = get_decision

    with pytest.raises(ValueError, match="разных проектов"):
        await service.create(
            project_id,
            from_decision.id,
            other_decision.id,
            DecisionLinkType.SEQUENTIAL,
        )

    mock_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_rejects_duplicate(
    service: DecisionLinkService,
    mock_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    project_id: UUID,
    from_decision: Decision,
    to_decision: Decision,
):
    """Связь того же типа между той же парой уже есть → ValueError."""
    def get_decision(id):
        if id == from_decision.id:
            return from_decision
        if id == to_decision.id:
            return to_decision
        return None

    mock_decision_repo.get_by_id.side_effect = get_decision
    mock_repo.list_by_project.return_value = [
        DecisionLink(
            project_id=project_id,
            from_decision_id=from_decision.id,
            to_decision_id=to_decision.id,
            link_type=DecisionLinkType.SEQUENTIAL,
        )
    ]

    with pytest.raises(ValueError, match="уже существует"):
        await service.create(
            project_id,
            from_decision.id,
            to_decision.id,
            DecisionLinkType.SEQUENTIAL,
        )

    mock_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_allows_same_pair_different_type(
    service: DecisionLinkService,
    mock_repo: AsyncMock,
    mock_decision_repo: AsyncMock,
    project_id: UUID,
    from_decision: Decision,
    to_decision: Decision,
):
    """Одна пара — разные типы связи: не дубль."""
    def get_decision(id):
        if id == from_decision.id:
            return from_decision
        if id == to_decision.id:
            return to_decision
        return None

    mock_decision_repo.get_by_id.side_effect = get_decision
    mock_repo.list_by_project.return_value = [
        DecisionLink(
            project_id=project_id,
            from_decision_id=from_decision.id,
            to_decision_id=to_decision.id,
            link_type=DecisionLinkType.SEQUENTIAL,
        )
    ]
    mock_repo.save.side_effect = lambda link: link

    result = await service.create(
        project_id,
        from_decision.id,
        to_decision.id,
        DecisionLinkType.PARALLEL,
    )

    assert result.link_type == DecisionLinkType.PARALLEL
    mock_repo.save.assert_called_once()


# ---------- Чтение и удаление ----------


@pytest.mark.asyncio
async def test_get_by_id(service: DecisionLinkService, mock_repo: AsyncMock):
    """get_by_id — делегирует в репозиторий."""
    link = DecisionLink(
        project_id=uuid4(),
        from_decision_id=uuid4(),
        to_decision_id=uuid4(),
        link_type=DecisionLinkType.NESTED,
    )
    mock_repo.get_by_id.return_value = link

    result = await service.get_by_id(link.id)

    assert result is link


@pytest.mark.asyncio
async def test_list_by_decision(service: DecisionLinkService, mock_repo: AsyncMock):
    """list_by_decision — делегирует в репозиторий."""
    decision_id = uuid4()
    mock_repo.list_by_decision.return_value = []

    result = await service.list_by_decision(decision_id)

    assert result == []
    mock_repo.list_by_decision.assert_called_once_with(decision_id)


@pytest.mark.asyncio
async def test_delete_success(service: DecisionLinkService, mock_repo: AsyncMock):
    """delete — найдено → True."""
    link = DecisionLink(
        project_id=uuid4(),
        from_decision_id=uuid4(),
        to_decision_id=uuid4(),
        link_type=DecisionLinkType.SEQUENTIAL,
    )
    mock_repo.get_by_id.return_value = link

    result = await service.delete(link.id)

    assert result is True
    mock_repo.delete.assert_called_once_with(link.id)


@pytest.mark.asyncio
async def test_delete_not_found(service: DecisionLinkService, mock_repo: AsyncMock):
    """delete — не найдено → False."""
    mock_repo.get_by_id.return_value = None

    result = await service.delete(uuid4())

    assert result is False
    mock_repo.delete.assert_not_called()
