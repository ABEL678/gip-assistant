"""Тесты DecisionService."""

from datetime import date
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from backend.src.domain.entities.decision import Decision
from backend.src.domain.entities.goal import Goal
from backend.src.domain.entities.premise import Premise
from backend.src.domain.entities.project import Project
from backend.src.domain.services.decision_service import DecisionService
from backend.src.domain.value_objects.enums import DecisionState, PremiseCategory, StageType


@pytest.fixture
def mock_decision_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.list_by_project = AsyncMock()
    repo.save = AsyncMock()
    repo.delete = AsyncMock()
    return repo


@pytest.fixture
def mock_project_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    return repo


@pytest.fixture
def mock_premise_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    return repo


@pytest.fixture
def mock_goal_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    return repo


@pytest.fixture
def service(
    mock_decision_repo: AsyncMock,
    mock_project_repo: AsyncMock,
    mock_premise_repo: AsyncMock,
    mock_goal_repo: AsyncMock,
) -> DecisionService:
    return DecisionService(
        mock_decision_repo,
        mock_project_repo,
        mock_premise_repo,
        mock_goal_repo,
    )


@pytest.fixture
def project() -> Project:
    return Project(name="Проект X", code="PRJ-X", stage=StageType.PD)


@pytest.fixture
def project_id(project: Project) -> UUID:
    return project.id


@pytest.fixture
def valid_decision(project_id: UUID) -> Decision:
    return Decision(
        id=uuid4(),
        project_id=project_id,
        formulation="Передать расчёт ВК на субподряд",
        state=DecisionState.PLAN,
    )


@pytest.fixture
def premise(project_id: UUID) -> Premise:
    return Premise(
        project_id=project_id,
        category=PremiseCategory.CONTRACT,
        name="Договор подряда",
    )


@pytest.fixture
def goal(project_id: UUID) -> Goal:
    return Goal(project_id=project_id, formulation="Сдать том 7 в экспертизу")


# ---------- Чтение ----------


@pytest.mark.asyncio
async def test_get(
    service: DecisionService, mock_decision_repo: AsyncMock, valid_decision: Decision,
):
    """get — находит решение по ID."""
    mock_decision_repo.get_by_id.return_value = valid_decision

    result = await service.get(valid_decision.id)

    assert result is valid_decision


@pytest.mark.asyncio
async def test_get_not_found(service: DecisionService, mock_decision_repo: AsyncMock):
    """get — возвращает None если не найдено."""
    mock_decision_repo.get_by_id.return_value = None

    result = await service.get(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_list_by_project(
    service: DecisionService, mock_decision_repo: AsyncMock, valid_decision: Decision,
):
    """list_by_project — возвращает список решений."""
    mock_decision_repo.list_by_project.return_value = [valid_decision]

    result = await service.list_by_project(valid_decision.project_id)

    assert len(result) == 1
    assert result[0].id == valid_decision.id


# ---------- Создание ----------


@pytest.mark.asyncio
async def test_create_success(
    service: DecisionService,
    mock_decision_repo: AsyncMock,
    mock_project_repo: AsyncMock,
    mock_premise_repo: AsyncMock,
    mock_goal_repo: AsyncMock,
    project: Project,
    premise: Premise,
    goal: Goal,
):
    """create — создаёт решение при успешной валидации."""
    mock_project_repo.get_by_id.return_value = project
    mock_premise_repo.get_by_id.return_value = premise
    mock_goal_repo.get_by_id.return_value = goal
    mock_decision_repo.save.side_effect = lambda d: d

    result = await service.create(
        project_id=project.id,
        formulation="Новое решение",
        premise_ids=[premise.id],
        goal_ids=[goal.id],
        rationale="Из договора",
        deadline=date(2026, 12, 1),
    )

    assert result.formulation == "Новое решение"
    assert result.premise_ids == [premise.id]
    assert result.goal_ids == [goal.id]
    assert result.rationale == "Из договора"
    mock_decision_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_empty_formulation(
    service: DecisionService, mock_decision_repo: AsyncMock,
):
    """create — пустая формулировка → ValueError."""
    with pytest.raises(ValueError, match="не может быть пустой"):
        await service.create(project_id=uuid4(), formulation="   ")

    mock_decision_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_project_not_found(
    service: DecisionService,
    mock_decision_repo: AsyncMock,
    mock_project_repo: AsyncMock,
):
    """create — проект не существует → ValueError."""
    mock_project_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Проект .* не найден"):
        await service.create(project_id=uuid4(), formulation="Решение")

    mock_decision_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_invalid_state(
    service: DecisionService,
    mock_decision_repo: AsyncMock,
    mock_project_repo: AsyncMock,
    project: Project,
):
    """create — недопустимое состояние → ValueError."""
    mock_project_repo.get_by_id.return_value = project

    with pytest.raises(ValueError, match="Недопустимое состояние"):
        await service.create(project_id=project.id, formulation="Решение", state="bogus")

    mock_decision_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_premise_not_found(
    service: DecisionService,
    mock_decision_repo: AsyncMock,
    mock_project_repo: AsyncMock,
    mock_premise_repo: AsyncMock,
    project: Project,
):
    """create — несуществующая вводная → ValueError."""
    mock_project_repo.get_by_id.return_value = project
    mock_premise_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Вводная .* не найдена"):
        await service.create(
            project_id=project.id,
            formulation="Решение",
            premise_ids=[uuid4()],
        )

    mock_decision_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_premise_wrong_project(
    service: DecisionService,
    mock_decision_repo: AsyncMock,
    mock_project_repo: AsyncMock,
    mock_premise_repo: AsyncMock,
    project: Project,
):
    """create — вводная из другого проекта → ValueError."""
    mock_project_repo.get_by_id.return_value = project
    other_premise = Premise(
        project_id=uuid4(),
        category=PremiseCategory.CONTRACT,
        name="Чужой договор",
    )
    mock_premise_repo.get_by_id.return_value = other_premise

    with pytest.raises(ValueError, match="принадлежит другому проекту"):
        await service.create(
            project_id=project.id,
            formulation="Решение",
            premise_ids=[other_premise.id],
        )

    mock_decision_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_goal_not_found(
    service: DecisionService,
    mock_decision_repo: AsyncMock,
    mock_project_repo: AsyncMock,
    mock_goal_repo: AsyncMock,
    project: Project,
):
    """create — несуществующая цель → ValueError."""
    mock_project_repo.get_by_id.return_value = project
    mock_goal_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Цель .* не найдена"):
        await service.create(
            project_id=project.id,
            formulation="Решение",
            goal_ids=[uuid4()],
        )

    mock_decision_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_goal_wrong_project(
    service: DecisionService,
    mock_decision_repo: AsyncMock,
    mock_project_repo: AsyncMock,
    mock_goal_repo: AsyncMock,
    project: Project,
):
    """create — цель из другого проекта → ValueError."""
    mock_project_repo.get_by_id.return_value = project
    other_goal = Goal(project_id=uuid4(), formulation="Чужая цель")
    mock_goal_repo.get_by_id.return_value = other_goal

    with pytest.raises(ValueError, match="принадлежит другому проекту"):
        await service.create(
            project_id=project.id,
            formulation="Решение",
            goal_ids=[other_goal.id],
        )

    mock_decision_repo.save.assert_not_called()


# ---------- Обновление ----------


@pytest.mark.asyncio
async def test_update_success(
    service: DecisionService,
    mock_decision_repo: AsyncMock,
    valid_decision: Decision,
):
    """update — обновляет поля решения."""
    mock_decision_repo.get_by_id.return_value = valid_decision
    mock_decision_repo.save.side_effect = lambda d: d

    result = await service.update(
        valid_decision.id,
        formulation="Обновлённое решение",
        state=DecisionState.ACCEPTED,
    )

    assert result.formulation == "Обновлённое решение"
    assert result.state == DecisionState.ACCEPTED
    mock_decision_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_update_not_found(
    service: DecisionService, mock_decision_repo: AsyncMock,
):
    """update — решение не найдено → ValueError."""
    mock_decision_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найдено"):
        await service.update(uuid4(), formulation="Новое")

    mock_decision_repo.save.assert_not_called()


# ---------- Удаление ----------


@pytest.mark.asyncio
async def test_delete_success(
    service: DecisionService,
    mock_decision_repo: AsyncMock,
    valid_decision: Decision,
):
    """delete — удаляет найденное решение."""
    mock_decision_repo.get_by_id.return_value = valid_decision

    await service.delete(valid_decision.id)

    mock_decision_repo.delete.assert_called_once_with(valid_decision.id)


@pytest.mark.asyncio
async def test_delete_not_found(
    service: DecisionService, mock_decision_repo: AsyncMock,
):
    """delete — решение не найдено → ValueError."""
    mock_decision_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="не найдено"):
        await service.delete(uuid4())

    mock_decision_repo.delete.assert_not_called()
