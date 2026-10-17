"""Smoke-тесты маппинга SQLAlchemy-моделей ↔ доменных сущностей Goal."""

import uuid

from backend.src.adapters.db.models.goal import GoalModel
from backend.src.adapters.db.models.goal_premise import GoalPremiseModel
from backend.src.adapters.db.repositories.goal_repository import (
    SqlAlchemyGoalRepository,
)
from backend.src.domain.entities.goal import Goal
from backend.src.domain.value_objects.enums import GoalState

# Создаём мок-репозиторий для вызова _to_domain (больше не staticmethod)
_mock_repo = SqlAlchemyGoalRepository.__new__(SqlAlchemyGoalRepository)


def test_goal_to_model_enum_value():
    """Domain → model: GoalState становится строкой 'plan'."""
    goal = Goal(
        project_id=uuid.uuid4(),
        formulation="Сдать том 7 в экспертизу",
        state=GoalState.PLAN,
    )
    model = SqlAlchemyGoalRepository._to_model(goal)

    assert model.state == "plan"
    assert isinstance(model.state, str)


def test_goal_to_domain_enum_value():
    """Model → domain: строка 'achieved' превращается в GoalState.ACHIEVED."""
    model = GoalModel(
        id=uuid.uuid4(),
        project_id=uuid.uuid4(),
        formulation="Цель достигнута",
        state="achieved",
    )
    goal = _mock_repo._to_domain(model)

    assert isinstance(goal.state, GoalState)
    assert goal.state == GoalState.ACHIEVED


def test_goal_roundtrip():
    """Domain → model → domain: все поля сохраняются."""
    project_id = uuid.uuid4()
    responsible_id = uuid.uuid4()
    created_by = uuid.uuid4()
    goal = Goal(
        id=uuid.uuid4(),
        project_id=project_id,
        formulation="Подготовить расчёт ВК",
        responsible_id=responsible_id,
        priority=3,
        state=GoalState.IN_PROGRESS,
        created_by=created_by,
    )
    model = SqlAlchemyGoalRepository._to_model(goal)
    goal2 = _mock_repo._to_domain(model)

    assert goal2.project_id == project_id
    assert goal2.formulation == "Подготовить расчёт ВК"
    assert goal2.responsible_id == responsible_id
    assert goal2.priority == 3
    assert goal2.state == GoalState.IN_PROGRESS
    assert goal2.created_by == created_by
    assert goal2.premise_ids == []


def test_goal_premise_model():
    """GoalPremiseModel: создание связи Goal ↔ Premise."""
    goal_id = uuid.uuid4()
    premise_id = uuid.uuid4()

    model = GoalPremiseModel(goal_id=goal_id, premise_id=premise_id)

    assert model.goal_id == goal_id
    assert model.premise_id == premise_id
    assert model.created_at is None  # server_default ставит БД
