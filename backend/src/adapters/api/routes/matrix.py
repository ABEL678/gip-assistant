"""Роуты матрицы смежников (ТЗ 3.0, раздел 5.2.2).

GET   /api/projects/{id}/matrix           — матрица проекта
POST  /api/projects/{id}/matrix/generate  — автогенерация
GET   /api/cross-tasks/{id}               — детали ячейки
PATCH /api/cross-tasks/{id}               — изменение статуса
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from backend.src.adapters.api.dependencies import (
    CrossTaskRepoDep,
    MatrixServiceDep,
    ProjectRepoDep,
)
from backend.src.application.dto.cross_task import (
    CrossTaskRead,
    CrossTaskUpdate,
)

router = APIRouter(prefix="/api", tags=["matrix"])


@router.get(
    "/projects/{project_id}/matrix",
    response_model=list[CrossTaskRead],
    summary="Матрица смежников проекта",
)
async def get_matrix(
    project_id: UUID,
    cross_task_repo: CrossTaskRepoDep,
) -> list[CrossTaskRead]:
    """Вернуть все ячейки матрицы проекта."""
    cross_tasks = await cross_task_repo.get_by_project(project_id)
    return [CrossTaskRead.model_validate(ct, from_attributes=True) for ct in cross_tasks]


@router.post(
    "/projects/{project_id}/matrix/generate",
    summary="Автогенерация матрицы смежников",
)
async def generate_matrix(
    project_id: UUID,
    project_repo: ProjectRepoDep,
    service: MatrixServiceDep,
) -> dict:
    """Сгенерировать матрицу для всех разделов проекта.

    Алгоритм:
    1. Собирает все уникальные `section_code` из задач проекта.
    2. Для каждой пары разделов (from → to), где from ≠ to,
       создаёт `CrossTask`, если её ещё нет.
    3. Возвращает количество созданных ячеек.
    """
    project = await project_repo.get_by_id(project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found",
        )

    created = await service.generate_matrix(project_id)

    return {
        "project_id": str(project_id),
        "cross_tasks_created": created,
    }


@router.get(
    "/cross-tasks/{cross_task_id}",
    response_model=CrossTaskRead,
    summary="Ячейка матрицы по ID",
)
async def get_cross_task(
    cross_task_id: UUID,
    repo: CrossTaskRepoDep,
) -> CrossTaskRead:
    cross_task = await repo.get_by_id(cross_task_id)
    if cross_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CrossTask {cross_task_id} not found",
        )
    return CrossTaskRead.model_validate(cross_task, from_attributes=True)


@router.patch(
    "/cross-tasks/{cross_task_id}",
    response_model=CrossTaskRead,
    summary="Обновить ячейку матрицы",
)
async def update_cross_task(
    cross_task_id: UUID,
    payload: CrossTaskUpdate,
    repo: CrossTaskRepoDep,
) -> CrossTaskRead:
    cross_task = await repo.get_by_id(cross_task_id)
    if cross_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CrossTask {cross_task_id} not found",
        )

    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(cross_task, field, value)

    saved = await repo.save(cross_task)
    return CrossTaskRead.model_validate(saved, from_attributes=True)
