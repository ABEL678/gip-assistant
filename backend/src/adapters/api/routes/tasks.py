"""Роуты задач.

GET   /api/projects/{id}/tasks        — список задач проекта
GET   /api/tasks/{id}                 — задача по ID
PATCH /api/tasks/{id}                 — inline-редактирование
GET   /api/cross-tasks/{id}/tasks     — задачи конкретной пары матрицы
"""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from backend.src.adapters.api.dependencies import CrossTaskRepoDep, TaskRepoDep
from backend.src.application.dto.task import (
    CrossTaskTaskRead,
    TaskRead,
    TaskUpdate,
)

router = APIRouter(prefix="/api", tags=["tasks"])


@router.get(
    "/projects/{project_id}/tasks",
    response_model=list[TaskRead],
    summary="Список задач проекта",
)
async def list_tasks(
    project_id: UUID,
    repo: TaskRepoDep,
    limit: int = 500,
    offset: int = 0,
) -> list[TaskRead]:
    tasks = await repo.get_by_project(project_id, limit=limit, offset=offset)
    return [TaskRead.model_validate(t, from_attributes=True) for t in tasks]


@router.get(
    "/tasks/{task_id}",
    response_model=TaskRead,
    summary="Задача по ID",
)
async def get_task(
    task_id: UUID,
    repo: TaskRepoDep,
) -> TaskRead:
    task = await repo.get_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    return TaskRead.model_validate(task, from_attributes=True)


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskRead,
    summary="Обновить задачу (inline)",
)
async def update_task(
    task_id: UUID,
    payload: TaskUpdate,
    repo: TaskRepoDep,
) -> TaskRead:
    task = await repo.get_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(task, field, value)

    saved = await repo.save(task)
    return TaskRead.model_validate(saved, from_attributes=True)


@router.get(
    "/cross-tasks/{cross_task_id}/tasks",
    response_model=list[CrossTaskTaskRead],
    summary="Задачи конкретной пары разделов (ячейки матрицы)",
)
async def list_cross_task_tasks(
    cross_task_id: UUID,
    cross_task_repo: CrossTaskRepoDep,
    task_repo: TaskRepoDep,
) -> list[CrossTaskTaskRead]:
    """Все задачи пары (from_section → to_section) с вычисленной просрочкой."""
    # 1. Найти cross_task
    cross_task = await cross_task_repo.get_by_id(cross_task_id)
    if cross_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CrossTask {cross_task_id} not found",
        )

    # 2. Найти задачи пары
    tasks = await task_repo.get_by_pair(
        cross_task.project_id,
        cross_task.from_section_code,
        cross_task.to_section_code,
    )

    # 3. Обогатить overdue_days
    today = date.today()
    result: list[CrossTaskTaskRead] = []
    for t in tasks:
        overdue_days = 0
        days_until = None
        if t.deadline:
            delta = (today - t.deadline).days
            if t.status not in ("DONE", "CANCELLED"):
                overdue_days = max(0, delta)
            days_until = -delta  # отрицательно если просрочено
        result.append(
            CrossTaskTaskRead(
                id=t.id,
                project_id=t.project_id,
                title=t.title,
                description=t.description,
                status=t.status,
                assignee_id=t.assignee_id,
                deadline=t.deadline,
                section_code=t.section_code,
                to_section_code=t.to_section_code,
                sort_order=t.sort_order,
                source=t.source,
                created_at=t.created_at,
                updated_at=t.updated_at,
                overdue_days=overdue_days,
                days_until_deadline=days_until,
            )
        )
    return result