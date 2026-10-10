"""Тесты MatrixService."""

from uuid import UUID, uuid4

import pytest
from unittest.mock import AsyncMock

from backend.src.domain.entities.task import Task
from backend.src.domain.services.matrix_service import MatrixService
from backend.src.domain.value_objects.enums import CrossTaskStatus, TaskStatus


@pytest.fixture
def cross_task_repo():
    return AsyncMock()


@pytest.fixture
def task_repo():
    return AsyncMock()


@pytest.fixture
def project_id() -> UUID:
    return uuid4()


# ---------- Успешные сценарии ----------


@pytest.mark.asyncio
async def test_matrix_two_sections_one_direction(cross_task_repo, task_repo, project_id):
    """2 раздела, задачи только в одну сторону (АР → ОВ) → 1 CrossTask."""
    task_repo.get_by_project.return_value = [
        Task(
            project_id=project_id,
            title="T1",
            section_code="АР",
            to_section_code="ОВ",
        ),
    ]
    cross_task_repo.find.return_value = None  # ничего не существует

    service = MatrixService(cross_task_repo, task_repo)
    count = await service.generate_matrix(project_id)

    assert count == 1
    cross_task_repo.save.assert_called_once()


@pytest.mark.asyncio
async def test_matrix_two_directions(cross_task_repo, task_repo, project_id):
    """2 раздела, задачи в обе стороны (АР → ОВ и ОВ → АР) → 2 CrossTask."""
    task_repo.get_by_project.return_value = [
        Task(
            project_id=project_id,
            title="T1",
            section_code="АР",
            to_section_code="ОВ",
        ),
        Task(
            project_id=project_id,
            title="T2",
            section_code="ОВ",
            to_section_code="АР",
        ),
    ]
    cross_task_repo.find.return_value = None

    service = MatrixService(cross_task_repo, task_repo)
    count = await service.generate_matrix(project_id)

    assert count == 2


@pytest.mark.asyncio
async def test_matrix_three_sections(cross_task_repo, task_repo, project_id):
    """3 раздела, 6 пар → 6 CrossTask."""
    pairs = [
        ("АР", "ОВ"),
        ("ОВ", "АР"),
        ("АР", "КР"),
        ("КР", "АР"),
        ("ОВ", "КР"),
        ("КР", "ОВ"),
    ]
    task_repo.get_by_project.return_value = [
        Task(
            project_id=project_id,
            title=f"T{i}",
            section_code=from_code,
            to_section_code=to_code,
        )
        for i, (from_code, to_code) in enumerate(pairs)
    ]
    cross_task_repo.find.return_value = None

    service = MatrixService(cross_task_repo, task_repo)
    count = await service.generate_matrix(project_id)

    assert count == 6


@pytest.mark.asyncio
async def test_matrix_aggregates_multiple_tasks(cross_task_repo, task_repo, project_id):
    """Несколько задач в одной паре → одна CrossTask."""
    task_repo.get_by_project.return_value = [
        Task(
            project_id=project_id,
            title=f"T{i}",
            section_code="АР",
            to_section_code="ОВ",
        )
        for i in range(5)
    ]
    cross_task_repo.find.return_value = None

    service = MatrixService(cross_task_repo, task_repo)
    count = await service.generate_matrix(project_id)

    # 5 задач одной пары → 1 CrossTask
    assert count == 1


@pytest.mark.asyncio
async def test_matrix_skips_diagonal(cross_task_repo, task_repo, project_id):
    """Задачи с section_code == to_section_code → пропускаются."""
    task_repo.get_by_project.return_value = [
        Task(
            project_id=project_id,
            title="T1",
            section_code="АР",
            to_section_code="АР",  # диагональ
        ),
    ]

    service = MatrixService(cross_task_repo, task_repo)
    count = await service.generate_matrix(project_id)

    assert count == 0


@pytest.mark.asyncio
async def test_matrix_skips_missing_to_section(cross_task_repo, task_repo, project_id):
    """Задачи без to_section_code → пропускаются."""
    task_repo.get_by_project.return_value = [
        Task(
            project_id=project_id,
            title="T1",
            section_code="АР",
            to_section_code=None,
        ),
    ]

    service = MatrixService(cross_task_repo, task_repo)
    count = await service.generate_matrix(project_id)

    assert count == 0


@pytest.mark.asyncio
async def test_matrix_one_section(cross_task_repo, task_repo, project_id):
    """Один раздел → нет пар → 0 CrossTask."""
    task_repo.get_by_project.return_value = [
        Task(
            project_id=project_id,
            title="T1",
            section_code="АР",
            to_section_code="АР",
        ),
    ]

    service = MatrixService(cross_task_repo, task_repo)
    count = await service.generate_matrix(project_id)

    assert count == 0


@pytest.mark.asyncio
async def test_matrix_no_sections(cross_task_repo, task_repo, project_id):
    """Нет задач → 0."""
    task_repo.get_by_project.return_value = []

    service = MatrixService(cross_task_repo, task_repo)
    count = await service.generate_matrix(project_id)

    assert count == 0


@pytest.mark.asyncio
async def test_matrix_idempotent(cross_task_repo, task_repo, project_id):
    """Повторный вызов не создаёт дубли."""
    task_repo.get_by_project.return_value = [
        Task(
            project_id=project_id,
            title="T1",
            section_code="АР",
            to_section_code="ОВ",
        ),
    ]
    # Первый вызов: не существует
    cross_task_repo.find.return_value = None

    service = MatrixService(cross_task_repo, task_repo)
    first = await service.generate_matrix(project_id)

    # Второй вызов: уже существует
    from backend.src.domain.entities.cross_task import CrossTask
    existing = CrossTask(
        project_id=project_id,
        from_section_code="АР",
        to_section_code="ОВ",
    )
    cross_task_repo.find.return_value = existing

    second = await service.generate_matrix(project_id)

    assert first == 1
    assert second == 0  # ничего не создалось заново