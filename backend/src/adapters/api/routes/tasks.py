"""Роуты задач.

GET   /api/projects/{id}/tasks    — список задач проекта
GET   /api/tasks/{id}             — задача по ID
PATCH /api/tasks/{id}             — inline-редактирование
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from backend.src.adapters.api.dependencies import TaskRepoDep
from backend.src.application.dto.task import TaskRead, TaskUpdate

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
    return [
        TaskRead.model_validate(t, from_attributes=True) for t in tasks
    ]


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

    # Применяем только заданные поля
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(task, field, value)

    saved = await repo.save(task)
    return TaskRead.model_validate(saved, from_attributes=True)
