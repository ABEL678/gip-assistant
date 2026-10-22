"""Smoke-тесты маппинга SQLAlchemy-моделей ↔ доменных сущностей Decision."""

import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from backend.src.adapters.db.models.decision import DecisionModel
from backend.src.adapters.db.models.decision_goal import DecisionGoalModel
from backend.src.adapters.db.models.decision_premise import DecisionPremiseModel
from backend.src.adapters.db.models.task import Task as TaskModel
from backend.src.adapters.db.repositories.decision_repository import (
    SqlAlchemyDecisionRepository,
)
from backend.src.domain.entities.decision import Decision
from backend.src.domain.entities.task import Task
from backend.src.domain.value_objects.enums import DecisionState

# Создаём мок-репозиторий для вызова _to_domain (больше не staticmethod)
_mock_repo = SqlAlchemyDecisionRepository.__new__(SqlAlchemyDecisionRepository)


def test_decision_to_model_enum_value():
    """Domain → model: DecisionState становится строкой 'plan'."""
    decision = Decision(
        project_id=uuid.uuid4(),
        formulation="Определить способ реализации",
        state=DecisionState.PLAN,
    )
    model = SqlAlchemyDecisionRepository._to_model(decision)

    assert model.state == "plan"
    assert isinstance(model.state, str)


def test_decision_to_domain_enum_value():
    """Model → domain: строка 'accepted' превращается в DecisionState.ACCEPTED."""
    model = DecisionModel(
        id=uuid.uuid4(),
        project_id=uuid.uuid4(),
        formulation="Принято решение",
        state="accepted",
    )
    decision = _mock_repo._to_domain(model)

    assert isinstance(decision.state, DecisionState)
    assert decision.state == DecisionState.ACCEPTED


def test_decision_all_enum_values():
    """Все 5 значений DecisionState маппятся корректно."""
    for enum_val in DecisionState:
        model = DecisionModel(
            id=uuid.uuid4(),
            project_id=uuid.uuid4(),
            formulation="Test",
            state=enum_val.value,
        )
        decision = _mock_repo._to_domain(model)
        assert decision.state == enum_val


def test_decision_roundtrip():
    """Domain → model → domain: все скалярные поля сохраняются."""
    project_id = uuid.uuid4()
    created_by = uuid.uuid4()
    decision = Decision(
        id=uuid.uuid4(),
        project_id=project_id,
        formulation="Обосновать срок",
        rationale="Срок из вводных",
        context="Контекст решения",
        deadline=uuid.UUID(int=1).date() if hasattr(uuid.UUID(int=1), 'date') else None,
        state=DecisionState.IN_PROGRESS,
        created_by=created_by,
    )
    model = SqlAlchemyDecisionRepository._to_model(decision)
    decision2 = _mock_repo._to_domain(model)

    assert decision2.project_id == project_id
    assert decision2.formulation == "Обосновать срок"
    assert decision2.rationale == "Срок из вводных"
    assert decision2.context == "Контекст решения"
    assert decision2.state == DecisionState.IN_PROGRESS
    assert decision2.created_by == created_by
    assert decision2.premise_ids == []
    assert decision2.goal_ids == []


def test_decision_goal_model():
    """DecisionGoalModel: создание связи Decision ↔ Goal."""
    decision_id = uuid.uuid4()
    goal_id = uuid.uuid4()

    model = DecisionGoalModel(decision_id=decision_id, goal_id=goal_id)

    assert model.decision_id == decision_id
    assert model.goal_id == goal_id
    assert model.created_at is None  # server_default ставит БД


def test_decision_premise_model():
    """DecisionPremiseModel: создание связи Decision ↔ Premise."""
    decision_id = uuid.uuid4()
    premise_id = uuid.uuid4()

    model = DecisionPremiseModel(decision_id=decision_id, premise_id=premise_id)

    assert model.decision_id == decision_id
    assert model.premise_id == premise_id
    assert model.created_at is None  # server_default ставит БД


@pytest.fixture
def mock_session() -> AsyncMock:
    """Мокированный AsyncSession."""
    session = AsyncMock()
    session.get = AsyncMock()
    session.merge = AsyncMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    session.add = MagicMock()
    # execute для _fetch_*_ids: select → []
    scalars_mock = MagicMock()
    scalars_mock.all.return_value = []
    result_mock = MagicMock()
    result_mock.scalars.return_value = scalars_mock
    session.execute = AsyncMock(return_value=result_mock)
    return session


@pytest.fixture
def repo(mock_session: AsyncMock) -> SqlAlchemyDecisionRepository:
    return SqlAlchemyDecisionRepository(mock_session)


@pytest.fixture
def decision() -> Decision:
    goal_ids = [uuid.uuid4(), uuid.uuid4()]
    premise_ids = [uuid.uuid4(), uuid.uuid4()]
    return Decision(
        id=uuid.uuid4(),
        project_id=uuid.uuid4(),
        formulation="Определить способ реализации",
        state=DecisionState.PLAN,
        goal_ids=goal_ids,
        premise_ids=premise_ids,
    )


@pytest.mark.asyncio
async def test_decision_save_with_goal_premise_ids(
    repo: SqlAlchemyDecisionRepository,
    mock_session: AsyncMock,
    decision: Decision,
):
    """save — сохраняет связи decision_goals и decision_premises."""
    model = SqlAlchemyDecisionRepository._to_model(decision)
    model.id = decision.id
    mock_session.merge.return_value = model
    mock_session.get.return_value = model

    await repo.save(decision)

    # Проверяем что add был вызван для новых связей
    assert mock_session.add.call_count == len(decision.goal_ids) + len(decision.premise_ids)


@pytest.mark.asyncio
async def test_decision_get_by_id_returns_goal_premise_ids(
    repo: SqlAlchemyDecisionRepository,
    mock_session: AsyncMock,
    decision: Decision,
):
    """get_by_id — возвращает decision с непустыми goal_ids и premise_ids."""
    model = SqlAlchemyDecisionRepository._to_model(decision)
    mock_session.get.return_value = model

    # Мокаем execute для _fetch_goal_ids и _fetch_premise_ids
    goal_ids = [uuid.uuid4(), uuid.uuid4()]
    premise_ids = [uuid.uuid4(), uuid.uuid4()]

    call_count = [0]

    async def mock_execute(stmt):
        call_count[0] += 1
        result_mock = MagicMock()
        if "goal_id" in str(stmt) or "decision_goals" in str(stmt):
            result_mock.scalars.return_value.all.return_value = goal_ids
        else:
            result_mock.scalars.return_value.all.return_value = premise_ids
        return result_mock

    mock_session.execute = AsyncMock(side_effect=mock_execute)

    result = await repo.get_by_id(decision.id)

    assert result is not None
    assert len(result.goal_ids) == 2
    assert len(result.premise_ids) == 2


def test_tasks_model_has_decision_id():
    """TaskModel: колонка decision_id существует."""
    task_model = TaskModel(
        id=uuid.uuid4(),
        project_id=uuid.uuid4(),
        title="Test task",
        decision_id=uuid.uuid4(),
    )
    assert task_model.decision_id is not None


def test_domain_task_has_decision_id():
    """Domain Task: поле decision_id существует."""
    task = Task(
        project_id=uuid.uuid4(),
        title="Test task",
        decision_id=uuid.uuid4(),
    )
    assert task.decision_id is not None
