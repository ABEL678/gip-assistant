"""Роуты для решений (Decision).

POST   /api/projects/{id}/decisions               — создать решение
GET    /api/projects/{id}/decisions               — список решений проекта
GET    /api/projects/{id}/decisions/proposals     — предложенные решения
POST   /api/projects/{id}/decisions/from-proposal — утвердить предложение
GET    /api/decisions/{id}                        — решение по ID
PATCH  /api/decisions/{id}                        — обновить решение
DELETE /api/decisions/{id}                        — удалить решение
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from backend.src.adapters.api.dependencies import (
    DecisionProposalServiceDep,
    DecisionServiceDep,
)
from backend.src.application.dto.decision import (
    DecisionCreate,
    DecisionProposal,
    DecisionProposalApprove,
    DecisionRead,
    DecisionUpdate,
)

router = APIRouter(prefix="/api", tags=["decisions"])


@router.post(
    "/projects/{project_id}/decisions",
    response_model=DecisionRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать решение в проекте",
)
async def create_decision(
    project_id: UUID,
    payload: DecisionCreate,
    service: DecisionServiceDep,
) -> DecisionRead:
    try:
        created = await service.create(
            project_id=project_id,
            formulation=payload.formulation,
            premise_ids=payload.premise_ids,
            goal_ids=payload.goal_ids,
            rationale=payload.rationale,
            context=payload.context,
            deadline=payload.deadline,
            state=payload.state,
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="conflict"
        ) from err
    return DecisionRead.model_validate(created, from_attributes=True)


@router.get(
    "/projects/{project_id}/decisions",
    response_model=list[DecisionRead],
    summary="Список решений проекта",
)
async def list_decisions(
    project_id: UUID,
    service: DecisionServiceDep,
) -> list[DecisionRead]:
    decisions = await service.list_by_project(project_id)
    return [DecisionRead.model_validate(d, from_attributes=True) for d in decisions]


# ---------- Proposals (ДО /{decision_id}!) ----------


@router.get(
    "/projects/{project_id}/decisions/proposals",
    response_model=list[DecisionProposal],
    summary="Предложенные решения (из целей)",
)
async def get_decision_proposals(
    project_id: UUID,
    service: DecisionProposalServiceDep,
) -> list[DecisionProposal]:
    proposals = await service.propose_decisions(project_id)
    return [DecisionProposal.model_validate(p, from_attributes=True) for p in proposals]


@router.post(
    "/projects/{project_id}/decisions/from-proposal",
    response_model=DecisionRead,
    status_code=status.HTTP_201_CREATED,
    summary="Утвердить предложенное решение",
)
async def approve_decision_proposal(
    project_id: UUID,
    payload: DecisionProposalApprove,
    service: DecisionServiceDep,
) -> DecisionRead:
    try:
        created = await service.create(
            project_id=project_id,
            formulation=payload.formulation,
            premise_ids=payload.premise_ids,
            goal_ids=payload.goal_ids,
            rationale=payload.rationale,
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="conflict"
        ) from err
    return DecisionRead.model_validate(created, from_attributes=True)


# ---------- Decisions (CRUD continued) ----------


@router.get(
    "/decisions/{decision_id}",
    response_model=DecisionRead,
    summary="Решение по ID",
)
async def get_decision(
    decision_id: UUID,
    service: DecisionServiceDep,
) -> DecisionRead:
    decision = await service.get(decision_id)
    if decision is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Decision {decision_id} not found",
        )
    return DecisionRead.model_validate(decision, from_attributes=True)


@router.patch(
    "/decisions/{decision_id}",
    response_model=DecisionRead,
    summary="Обновить решение",
)
async def update_decision(
    decision_id: UUID,
    payload: DecisionUpdate,
    service: DecisionServiceDep,
) -> DecisionRead:
    data = payload.model_dump(exclude_unset=True, by_alias=False)
    try:
        updated = await service.update(decision_id, **data)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Decision {decision_id} not found",
        )
    return DecisionRead.model_validate(updated, from_attributes=True)


@router.delete(
    "/decisions/{decision_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить решение",
)
async def delete_decision(
    decision_id: UUID,
    service: DecisionServiceDep,
) -> None:
    try:
        await service.delete(decision_id)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
