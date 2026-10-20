"""Роуты для действий (Action).

POST   /api/projects/{id}/actions               — создать действие
GET    /api/projects/{id}/actions                — список действий проекта
GET    /api/tasks/{task_id}/actions              — список действий задачи
GET    /api/actions/{id}                         — действие по ID
PATCH  /api/actions/{id}                         — обновить действие
DELETE /api/actions/{id}                         — удалить действие
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from backend.src.adapters.api.dependencies import ActionServiceDep
from backend.src.application.dto.action import (
    ActionCreate,
    ActionRead,
    ActionUpdate,
)

router = APIRouter(prefix="/api", tags=["actions"])


@router.post(
    "/projects/{project_id}/actions",
    response_model=ActionRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать действие в проекте",
)
async def create_action(
    project_id: UUID,
    payload: ActionCreate,
    service: ActionServiceDep,
) -> ActionRead:
    try:
        created = await service.create(
            project_id=project_id,
            formulation=payload.formulation,
            task_id=payload.task_id,
            measurable_result=payload.measurable_result,
            deadline=payload.deadline,
            responsible_id=payload.responsible_id,
            state=payload.state,
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    return ActionRead.model_validate(created, from_attributes=True)


@router.get(
    "/projects/{project_id}/actions",
    response_model=list[ActionRead],
    summary="Список действий проекта",
)
async def list_actions(
    project_id: UUID,
    service: ActionServiceDep,
) -> list[ActionRead]:
    actions = await service.list_by_project(project_id)
    return [ActionRead.model_validate(a, from_attributes=True) for a in actions]


@router.get(
    "/tasks/{task_id}/actions",
    response_model=list[ActionRead],
    summary="Список действий задачи",
)
async def list_by_task(
    task_id: UUID,
    service: ActionServiceDep,
) -> list[ActionRead]:
    actions = await service.list_by_task(task_id)
    return [ActionRead.model_validate(a, from_attributes=True) for a in actions]


@router.get(
    "/actions/{action_id}",
    response_model=ActionRead,
    summary="Действие по ID",
)
async def get_action(
    action_id: UUID,
    service: ActionServiceDep,
) -> ActionRead:
    action = await service.get_by_id(action_id)
    if action is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Action {action_id} not found",
        )
    return ActionRead.model_validate(action, from_attributes=True)


@router.patch(
    "/actions/{action_id}",
    response_model=ActionRead,
    summary="Обновить действие",
)
async def update_action(
    action_id: UUID,
    payload: ActionUpdate,
    service: ActionServiceDep,
) -> ActionRead:
    data = payload.model_dump(exclude_unset=True)
    try:
        updated = await service.update(action_id, **data)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Action {action_id} not found",
        )
    return ActionRead.model_validate(updated, from_attributes=True)


@router.delete(
    "/actions/{action_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить действие",
)
async def delete_action(
    action_id: UUID,
    service: ActionServiceDep,
) -> None:
    try:
        await service.delete(action_id)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
