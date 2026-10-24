"""RfiService — CRUD + валидации (spec_week_4.md §6)."""

from datetime import date
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from backend.src.domain.services.rfi_service import RfiService
from backend.src.domain.value_objects.enums import RfiState, TaskStatus


def _make_project_repo(project_id):
    repo = AsyncMock()
    project = AsyncMock(id=project_id)
    repo.get_by_id.return_value = project
    return repo


def _make_decision_repo(decision_id, project_id):
    repo = AsyncMock()
    decision = AsyncMock(id=decision_id, project_id=project_id)
    repo.get_by_id.return_value = decision
    return repo


def _make_goal_repo(goal_id, project_id):
    repo = AsyncMock()
    goal = AsyncMock(id=goal_id, project_id=project_id)
    repo.get_by_id.return_value = goal
    return repo


def _make_task_repo():
    repo = AsyncMock()
    repo.save.side_effect = lambda t: t
    return repo


def _make_rfi_repo():
    repo = AsyncMock()
    repo.list_rfis_by_project.return_value = []
    return repo


@pytest.mark.asyncio
async def test_create_rfi_with_decision():
    """Создание RFI с причиной — решение."""
    project_id = uuid4()
    decision_id = uuid4()
    task_repo = _make_task_repo()
    project_repo = _make_project_repo(project_id)
    decision_repo = _make_decision_repo(decision_id, project_id)
    rfi_repo = _make_rfi_repo()

    service = RfiService(
        task_repo=task_repo,
        project_repo=project_repo,
        decision_repo=decision_repo,
        goal_repo=AsyncMock(),
        rfi_repo=rfi_repo,
    )

    result = await service.create(
        project_id=project_id,
        title="Запросить ИД",
        rfi_cause_decision_id=decision_id,
        rfi_due_date=date(2026, 12, 31),
    )

    assert result.is_rfi is True
    assert result.rfi_cause_decision_id == decision_id
    assert result.rfi_state == RfiState.OPEN
    assert result.status == TaskStatus.NOT_STARTED
    task_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_rfi_with_goal():
    """Создание RFI с причиной — цель."""
    project_id = uuid4()
    goal_id = uuid4()
    task_repo = _make_task_repo()
    project_repo = _make_project_repo(project_id)
    goal_repo = _make_goal_repo(goal_id, project_id)
    rfi_repo = _make_rfi_repo()

    service = RfiService(
        task_repo=task_repo,
        project_repo=project_repo,
        decision_repo=AsyncMock(),
        goal_repo=goal_repo,
        rfi_repo=rfi_repo,
    )

    result = await service.create(
        project_id=project_id,
        title="Запросить данные",
        rfi_cause_goal_id=goal_id,
    )

    assert result.is_rfi is True
    assert result.rfi_cause_goal_id == goal_id
    task_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_rfi_no_reason():
    """Без причины — ValueError."""
    service = RfiService(
        task_repo=AsyncMock(),
        project_repo=AsyncMock(),
        decision_repo=AsyncMock(),
        goal_repo=AsyncMock(),
        rfi_repo=AsyncMock(),
    )
    with pytest.raises(ValueError, match="XOR"):
        await service.create(
            project_id=uuid4(),
            title="Без причины",
        )


@pytest.mark.asyncio
async def test_create_rfi_both_reasons():
    """Две причины — ValueError."""
    service = RfiService(
        task_repo=AsyncMock(),
        project_repo=AsyncMock(),
        decision_repo=AsyncMock(),
        goal_repo=AsyncMock(),
        rfi_repo=AsyncMock(),
    )
    with pytest.raises(ValueError, match="XOR"):
        await service.create(
            project_id=uuid4(),
            title="Две причины",
            rfi_cause_decision_id=uuid4(),
            rfi_cause_goal_id=uuid4(),
        )


@pytest.mark.asyncio
async def test_create_rfi_wrong_project():
    """Причина из другого проекта — ValueError."""
    project_id = uuid4()
    other_id = uuid4()
    service = RfiService(
        task_repo=AsyncMock(),
        project_repo=_make_project_repo(project_id),
        decision_repo=_make_decision_repo(other_id, other_id),
        goal_repo=AsyncMock(),
        rfi_repo=AsyncMock(),
    )
    with pytest.raises(ValueError, match="другому проекту"):
        await service.create(
            project_id=project_id,
            title="Не тот проект",
            rfi_cause_decision_id=other_id,
        )


@pytest.mark.asyncio
async def test_get_rfi_not_found():
    """Не-RFI Task → None."""
    task_repo = AsyncMock()
    task_repo.get_by_id.return_value = AsyncMock(is_rfi=False)
    service = RfiService(
        task_repo=task_repo,
        project_repo=AsyncMock(),
        decision_repo=AsyncMock(),
        goal_repo=AsyncMock(),
        rfi_repo=AsyncMock(),
    )
    result = await service.get(uuid4())
    assert result is None


@pytest.mark.asyncio
async def test_escalate():
    """Эскалация RFI."""
    rfi = AsyncMock(is_rfi=True)
    task_repo = AsyncMock()
    task_repo.get_by_id.return_value = rfi
    task_repo.save.side_effect = lambda t: t
    service = RfiService(
        task_repo=task_repo,
        project_repo=AsyncMock(),
        decision_repo=AsyncMock(),
        goal_repo=AsyncMock(),
        rfi_repo=AsyncMock(),
    )
    result = await service.escalate(uuid4())
    assert result.rfi_state == RfiState.ESCALATED


@pytest.mark.asyncio
async def test_list_by_project():
    """Список RFI проекта через rfi_repo."""
    project_id = uuid4()
    rfi = AsyncMock(is_rfi=True)
    rfi_repo = _make_rfi_repo()
    rfi_repo.list_rfis_by_project.return_value = [rfi]

    service = RfiService(
        task_repo=AsyncMock(),
        project_repo=AsyncMock(),
        decision_repo=AsyncMock(),
        goal_repo=AsyncMock(),
        rfi_repo=rfi_repo,
    )
    result = await service.list_by_project(project_id)

    assert result == [rfi]
    rfi_repo.list_rfis_by_project.assert_called_once_with(project_id)


@pytest.mark.asyncio
async def test_update_rfi():
    """Обновление RFI."""
    rfi = AsyncMock(
        is_rfi=True,
        project_id=uuid4(),
        rfi_cause_decision_id=uuid4(),
        rfi_cause_goal_id=None,
    )
    task_repo = AsyncMock()
    task_repo.get_by_id.return_value = rfi
    task_repo.save.side_effect = lambda t: t
    service = RfiService(
        task_repo=task_repo,
        project_repo=AsyncMock(),
        decision_repo=AsyncMock(),
        goal_repo=AsyncMock(),
        rfi_repo=AsyncMock(),
    )
    result = await service.update(rfi.id, title="Новый заголовок")
    assert result.title == "Новый заголовок"
    task_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_update_rfi_wrong_xor():
    """Обновление: одна причина → обе причины → ValueError."""
    project_id = uuid4()
    rfi = AsyncMock(
        is_rfi=True,
        project_id=project_id,
        rfi_cause_decision_id=uuid4(),
        rfi_cause_goal_id=None,
    )
    task_repo = AsyncMock()
    task_repo.get_by_id.return_value = rfi
    service = RfiService(
        task_repo=task_repo,
        project_repo=AsyncMock(),
        decision_repo=AsyncMock(),
        goal_repo=AsyncMock(),
        rfi_repo=AsyncMock(),
    )
    with pytest.raises(ValueError, match="XOR"):
        await service.update(
            rfi.id,
            rfi_cause_decision_id=uuid4(),
            rfi_cause_goal_id=uuid4(),
        )


@pytest.mark.asyncio
async def test_delete_rfi():
    """Удаление RFI."""
    rfi = AsyncMock(is_rfi=True)
    task_repo = AsyncMock()
    task_repo.get_by_id.return_value = rfi
    service = RfiService(
        task_repo=task_repo,
        project_repo=AsyncMock(),
        decision_repo=AsyncMock(),
        goal_repo=AsyncMock(),
        rfi_repo=AsyncMock(),
    )
    await service.delete(rfi.id)
    task_repo.delete.assert_called_once_with(rfi.id)


@pytest.mark.asyncio
async def test_update_rfi_wrong_project():
    """Обновление: причина из другого проекта → ValueError."""
    project_id = uuid4()
    other_id = uuid4()
    rfi = AsyncMock(
        is_rfi=True,
        project_id=project_id,
        rfi_cause_decision_id=None,
        rfi_cause_goal_id=None,
    )
    task_repo = AsyncMock()
    task_repo.get_by_id.return_value = rfi
    decision_repo = _make_decision_repo(other_id, other_id)
    service = RfiService(
        task_repo=task_repo,
        project_repo=AsyncMock(),
        decision_repo=decision_repo,
        goal_repo=AsyncMock(),
        rfi_repo=AsyncMock(),
    )
    with pytest.raises(ValueError, match="другому проекту"):
        await service.update(
            rfi.id,
            rfi_cause_decision_id=other_id,
        )


@pytest.mark.asyncio
async def test_delete_non_rfi_raises():
    """Удаление не-RFI Task → ValueError."""
    task_repo = AsyncMock()
    task_repo.get_by_id.return_value = AsyncMock(is_rfi=False)
    service = RfiService(
        task_repo=task_repo,
        project_repo=AsyncMock(),
        decision_repo=AsyncMock(),
        goal_repo=AsyncMock(),
        rfi_repo=AsyncMock(),
    )
    with pytest.raises(ValueError, match="не найден"):
        await service.delete(uuid4())
