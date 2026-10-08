"""Тесты MatrixService."""

import pytest

from backend.src.domain.entities.task import Task
from backend.src.domain.services.matrix_service import MatrixService


@pytest.mark.asyncio
async def test_matrix_two_sections(cross_task_repo, task_repo, project_id):
    """2 раздела → 2 CrossTask (A→B и B→A)."""
    task_repo.get_by_project.return_value = [
        Task(project_id=project_id, title="T1", section_code="ОВ"),
        Task(project_id=project_id, title="T2", section_code="АР"),
    ]
    service = MatrixService(cross_task_repo, task_repo)

    count = await service.generate_matrix(project_id)

    assert count == 2


@pytest.mark.asyncio
async def test_matrix_three_sections(cross_task_repo, task_repo, project_id):
    """3 раздела → 6 CrossTask (3 * 2)."""
    task_repo.get_by_project.return_value = [
        Task(project_id=project_id, title="T1", section_code="ОВ"),
        Task(project_id=project_id, title="T2", section_code="АР"),
        Task(project_id=project_id, title="T3", section_code="КР"),
    ]
    service = MatrixService(cross_task_repo, task_repo)

    count = await service.generate_matrix(project_id)

    assert count == 6  # 3 раздела * (3 - 1) = 6


@pytest.mark.asyncio
async def test_matrix_one_section(cross_task_repo, task_repo, project_id):
    """1 раздел → 0 CrossTask."""
    task_repo.get_by_project.return_value = [
        Task(project_id=project_id, title="T1", section_code="ОВ"),
    ]
    service = MatrixService(cross_task_repo, task_repo)

    count = await service.generate_matrix(project_id)

    assert count == 0


@pytest.mark.asyncio
async def test_matrix_no_sections(cross_task_repo, task_repo, project_id):
    """Задачи без section_code → 0 CrossTask."""
    task_repo.get_by_project.return_value = [
        Task(project_id=project_id, title="T1"),  # section_code=None
        Task(project_id=project_id, title="T2"),
    ]
    service = MatrixService(cross_task_repo, task_repo)

    count = await service.generate_matrix(project_id)

    assert count == 0


@pytest.mark.asyncio
async def test_matrix_idempotent(cross_task_repo, task_repo, project_id):
    """Повторный вызов не создаёт дубли."""
    task_repo.get_by_project.return_value = [
        Task(project_id=project_id, title="T1", section_code="ОВ"),
        Task(project_id=project_id, title="T2", section_code="АР"),
    ]
    service = MatrixService(cross_task_repo, task_repo)

    first = await service.generate_matrix(project_id)
    second = await service.generate_matrix(project_id)

    assert first == 2
    assert second == 0  # уже есть


@pytest.mark.asyncio
async def test_matrix_five_sections(cross_task_repo, task_repo, project_id):
    """5 разделов → 20 CrossTask (5 * 4)."""
    task_repo.get_by_project.return_value = [
        Task(project_id=project_id, title=f"T{i}", section_code=f"S{i}") for i in range(5)
    ]
    service = MatrixService(cross_task_repo, task_repo)

    count = await service.generate_matrix(project_id)

    assert count == 20
