"""Роуты для целей (Goal).

POST   /api/projects/{id}/goals                     — создать цель
GET    /api/projects/{id}/goals                     — список целей проекта
GET    /api/projects/{id}/goals/proposals           — предложенные цели
POST   /api/projects/{id}/goals/from-proposal       — утвердить предложение
GET    /api/goals/{id}                              — цель по ID
PATCH  /api/goals/{id}                              — обновить цель
DELETE /api/goals/{id}                              — удалить цель
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from backend.src.adapters.api.dependencies import (
    GoalProposalServiceDep,
    GoalServiceDep,
)
from backend.src.application.dto.goal import (
    GoalCreate,
    GoalProposalApprove,
    GoalProposalRead,
    GoalRead,
    GoalUpdate,
)

router = APIRouter(prefix="/api", tags=["goals"])


# ---------- Goals (CRUD) ----------


@router.post(
    "/projects/{project_id}/goals",
    response_model=GoalRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать цель в проекте",
)
async def create_goal(
    project_id: UUID,
    payload: GoalCreate,
    service: GoalServiceDep,
) -> GoalRead:
    try:
        created = await service.create(
            project_id=project_id,
            formulation=payload.formulation,
            premise_ids=payload.premise_ids,
            deadline=payload.deadline,
            responsible_id=payload.responsible_id,
            priority=payload.priority,
            state=payload.state,
            created_by=payload.created_by,
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    return GoalRead.model_validate(created, from_attributes=True)


@router.get(
    "/projects/{project_id}/goals",
    response_model=list[GoalRead],
    summary="Список целей проекта",
)
async def list_goals(
    project_id: UUID,
    service: GoalServiceDep,
) -> list[GoalRead]:
    goals = await service.list_by_project(project_id)
    return [GoalRead.model_validate(g, from_attributes=True) for g in goals]


# ---------- Proposals (ДО /{goal_id}!) ----------


@router.get(
    "/projects/{project_id}/goals/proposals",
    response_model=list[GoalProposalRead],
    summary="Предложенные цели (из вводных)",
)
async def get_goal_proposals(
    project_id: UUID,
    service: GoalProposalServiceDep,
) -> list[GoalProposalRead]:
    proposals = await service.propose_goals(project_id)
    return [
        GoalProposalRead.model_validate(p, from_attributes=True)
        for p in proposals
    ]


@router.post(
    "/projects/{project_id}/goals/from-proposal",
    response_model=GoalRead,
    status_code=status.HTTP_201_CREATED,
    summary="Утвердить предложенную цель",
)
async def approve_goal_proposal(
    project_id: UUID,
    payload: GoalProposalApprove,
    service: GoalServiceDep,
) -> GoalRead:
    try:
        created = await service.create(
            project_id=project_id,
            formulation=payload.formulation,
            premise_ids=payload.premise_ids,
            deadline=payload.deadline,
            priority=payload.priority,
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    return GoalRead.model_validate(created, from_attributes=True)


# ---------- Goals (CRUD continued) ----------


@router.get(
    "/goals/{goal_id}",
    response_model=GoalRead,
    summary="Цель по ID",
)
async def get_goal(
    goal_id: UUID,
    service: GoalServiceDep,
) -> GoalRead:
    goal = await service.get(goal_id)
    if goal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Goal {goal_id} not found",
        )
    return GoalRead.model_validate(goal, from_attributes=True)


@router.patch(
    "/goals/{goal_id}",
    response_model=GoalRead,
    summary="Обновить цель",
)
async def update_goal(
    goal_id: UUID,
    payload: GoalUpdate,
    service: GoalServiceDep,
) -> GoalRead:
    data = payload.model_dump(exclude_unset=True, by_alias=False)
    try:
        updated = await service.update(goal_id, **data)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Goal {goal_id} not found",
        )
    return GoalRead.model_validate(updated, from_attributes=True)


@router.delete(
    "/goals/{goal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить цель",
)
async def delete_goal(
    goal_id: UUID,
    service: GoalServiceDep,
) -> None:
    try:
        await service.delete(goal_id)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
