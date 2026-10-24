"""Интеграционный тест: RFI + Document(rfi_id) + 2 Premise(source_document_id)
→ _fetch_premise_ids → 2 UUID.

Репозиторий-level (AsyncSessionLocal + реальные репозитории),
не httpx. Требует запущенный PostgreSQL (прецедент 6.8a).
httpx-версия — 6.12c (когда будут роуты).
"""

from uuid import uuid4

import pytest

from backend.src.adapters.db.models.document import DocumentModel
from backend.src.adapters.db.models.document_type import DocumentTypeModel
from backend.src.adapters.db.models.goal import GoalModel
from backend.src.adapters.db.models.premise import PremiseModel
from backend.src.adapters.db.models.project import Project
from backend.src.adapters.db.models.task import Task as TaskModel
from backend.src.adapters.db.repositories.task_repo import SqlAlchemyTaskRepository
from backend.src.adapters.db.session import AsyncSessionLocal
from backend.src.domain.value_objects.document import (
    DocumentKind,
    LifecycleStatus,
)
from backend.src.domain.value_objects.enums import PremiseCategory, RfiState


@pytest.fixture
async def session():
    """Сессия с nested-транзакцией для изоляции.

    BEGIN → SAVEPOINT → yield → ROLLBACK TO SAVEPOINT → COMMIT (пустой).
    Данные не утекают в БД, т.к. транзакция теста (если есть)
    делает rollback после завершения.
    """
    async with AsyncSessionLocal() as s:
        async with s.begin():
            # Используем SAVEPOINT для изоляции
            savepoint = await s.begin_nested()
            yield s
            await savepoint.rollback()


@pytest.mark.asyncio(loop_scope="function")
async def test_rfi_premise_ids_persist_end_to_end(session):
    """Создать RFI + Document(rfi_id) + 2 Premise(source_document_id)
    → get_rfi_by_id → task.premise_ids = 2 UUID.
    """
    project_id = uuid4()
    document_type_id = uuid4()

    # 0. Создаём Project
    project = Project(
        id=project_id,
        name="Test Project",
        code="TEST-001",
        stage="PD",
    )
    session.add(project)

    # 0.1. Создаём DocumentType для FK document_type_id
    doc_type = DocumentTypeModel(
        id=document_type_id,
        code=f"TEST-DT-{uuid4().hex[:8]}",
        name="Test Document Type",
    )
    session.add(doc_type)
    await session.flush()

    # 0.2. Создаём Goal для rfi_cause_goal_id FK
    goal_id = uuid4()
    goal = GoalModel(
        id=goal_id,
        project_id=project_id,
        formulation="Test goal",
    )
    session.add(goal)
    await session.flush()

    # 1. Создаём RFI Task
    rfi_id = uuid4()
    rfi = TaskModel(
        id=rfi_id,
        project_id=project_id,
        title="Запросить ИД для решения",
        is_rfi=True,
        rfi_cause_goal_id=goal_id,
        rfi_state=RfiState.OPEN,
        status="NOT_STARTED",
        sort_order=0,
        source="manual",
    )
    session.add(rfi)
    await session.flush()

    # 2. Создаём Document с rfi_id
    doc_id = uuid4()
    doc = DocumentModel(
        id=doc_id,
        guid=uuid4(),
        project_id=project_id,
        document_type_id=document_type_id,
        document_name="Ответ на RFI",
        cipher="TEST-001",
        document_kind=DocumentKind.PD.value,
        lifecycle_status=LifecycleStatus.DRAFT.value,
        rfi_id=rfi_id,
    )
    session.add(doc)
    await session.flush()

    # 3. Создаём 2 Premise с source_document_id
    p1_id = uuid4()
    p1 = PremiseModel(
        id=p1_id,
        project_id=project_id,
        category=PremiseCategory.SOURCE_DATA,
        name="Нагрузки на ВК",
        source_document_id=doc_id,
    )
    session.add(p1)

    p2_id = uuid4()
    p2 = PremiseModel(
        id=p2_id,
        project_id=project_id,
        category=PremiseCategory.SOURCE_DATA,
        name="Нагрузки на АР",
        source_document_id=doc_id,
    )
    session.add(p2)
    await session.flush()

    # 4. Проверяем через _fetch_premise_ids
    task_repo = SqlAlchemyTaskRepository(session)
    task = await task_repo.get_by_id(rfi_id)

    assert task is not None
    assert task.is_rfi is True
    assert len(task.premise_ids) == 2
    assert set(task.premise_ids) == {p1_id, p2_id}
