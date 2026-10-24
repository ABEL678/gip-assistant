"""Smoke-тесты маппинга Task RFI полей (6.12a)."""

from datetime import date
from uuid import uuid4

from backend.src.adapters.db.models.task import Task as TaskModel
from backend.src.adapters.db.repositories.task_repo import SqlAlchemyTaskRepository
from backend.src.domain.entities.task import Task
from backend.src.domain.value_objects.enums import RfiState


def test_task_rfi_to_model():
    """Domain → model: все 5 полей корректно маппятся."""
    task = Task(
        project_id=uuid4(),
        title="test",
        is_rfi=True,
        rfi_cause_decision_id=uuid4(),
        rfi_cause_goal_id=uuid4(),
        rfi_due_date=date(2026, 12, 31),
        rfi_state=RfiState.OPEN,
    )
    model = SqlAlchemyTaskRepository._to_model(task)
    assert model.is_rfi is True
    assert model.rfi_cause_decision_id == task.rfi_cause_decision_id
    assert model.rfi_cause_goal_id == task.rfi_cause_goal_id
    assert model.rfi_due_date == task.rfi_due_date
    assert model.rfi_state == "open"


def test_task_rfi_to_domain():
    """Model → domain: все 5 полей корректно маппятся."""
    model = TaskModel(
        id=uuid4(),
        project_id=uuid4(),
        title="test",
        is_rfi=True,
        rfi_cause_decision_id=uuid4(),
        rfi_cause_goal_id=uuid4(),
        rfi_due_date=date(2026, 12, 31),
        rfi_state="sent",
    )
    task = SqlAlchemyTaskRepository._to_domain(model)
    assert task.is_rfi is True
    assert task.rfi_cause_decision_id == model.rfi_cause_decision_id
    assert task.rfi_cause_goal_id == model.rfi_cause_goal_id
    assert task.rfi_due_date == model.rfi_due_date
    assert task.rfi_state == RfiState.SENT


def test_task_non_rfi_defaults():
    """Не-RFI Task: is_rfi=False, все rfi_* = None."""
    task = Task(project_id=uuid4(), title="test")
    model = SqlAlchemyTaskRepository._to_model(task)
    assert model.is_rfi is False
    assert model.rfi_cause_decision_id is None
    assert model.rfi_cause_goal_id is None
    assert model.rfi_due_date is None
    assert model.rfi_state is None


def test_task_non_rfi_to_domain():
    """Не-RFI модель → domain: rfi_state = None."""
    model = TaskModel(
        id=uuid4(),
        project_id=uuid4(),
        title="test",
        is_rfi=False,
        rfi_state=None,
    )
    task = SqlAlchemyTaskRepository._to_domain(model)
    assert task.is_rfi is False
    assert task.rfi_state is None


def test_task_rfi_roundtrip():
    """Domain → model → domain: поля не теряются."""
    original = Task(
        project_id=uuid4(),
        title="rfi test",
        is_rfi=True,
        rfi_cause_decision_id=uuid4(),
        rfi_cause_goal_id=None,
        rfi_due_date=date(2026, 11, 15),
        rfi_state=RfiState.ESCALATED,
    )
    model = SqlAlchemyTaskRepository._to_model(original)
    restored = SqlAlchemyTaskRepository._to_domain(model)
    assert restored.is_rfi == original.is_rfi
    assert restored.rfi_cause_decision_id == original.rfi_cause_decision_id
    assert restored.rfi_cause_goal_id == original.rfi_cause_goal_id
    assert restored.rfi_due_date == original.rfi_due_date
    assert restored.rfi_state == original.rfi_state
