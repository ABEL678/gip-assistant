"""Роуты для RFI (Task с is_rfi=true).

GET    /api/projects/{id}/rfis/proposals              — предложения RFI
POST   /api/projects/{id}/rfis/from-proposal          — утвердить предложение (создать RFI)
GET    /api/projects/{id}/rfis                         — список RFI
POST   /api/projects/{id}/rfis                         — создать RFI
GET    /api/rfis/{id}                                  — RFI по ID
PATCH  /api/rfis/{id}                                  — обновить RFI
DELETE /api/rfis/{id}                                  — удалить RFI
POST   /api/rfis/{id}/escalate                         — эскалировать RFI
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from backend.src.adapters.api.dependencies import (
    RfiProposalServiceDep,
    RfiServiceDep,
)
from backend.src.application.dto.rfi import (
    RfiCreate,
    RfiProposal,
    RfiProposalApprove,
    RfiRead,
    RfiUpdate,
)
from backend.src.domain.value_objects.enums import RfiState

router = APIRouter(prefix="/api", tags=["rfis"])


# ---------- Proposals (ДО /{rfi_id}!) ----------


@router.get(
    "/projects/{project_id}/rfis/proposals",
    response_model=list[RfiProposal],
    summary="Предложенные RFI (из правил)",
)
async def list_rfis_proposals(
    project_id: UUID,
    service: RfiProposalServiceDep,
) -> list[RfiProposal]:
    return await service.propose_rfis(project_id)


@router.post(
    "/projects/{project_id}/rfis/from-proposal",
    response_model=RfiRead,
    status_code=status.HTTP_201_CREATED,
    summary="Утвердить предложенный RFI (создать)",
)
async def create_rfi_from_proposal(
    project_id: UUID,
    payload: RfiProposalApprove,
    service: RfiServiceDep,
) -> RfiRead:
    # formulation → title, rationale → description
    try:
        task = await service.create(
            project_id=project_id,
            title=payload.formulation,
            rfi_cause_decision_id=payload.rfi_cause_decision_id,
            rfi_due_date=payload.rfi_due_date,
            rfi_state=payload.rfi_state,
            description=payload.rationale,
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="conflict"
        ) from err
    return RfiRead.model_validate(task, from_attributes=True)


# ---------- RFI CRUD ----------


@router.get(
    "/projects/{project_id}/rfis",
    response_model=list[RfiRead],
    summary="Список RFI проекта",
)
async def list_rfis(
    project_id: UUID,
    service: RfiServiceDep,
) -> list[RfiRead]:
    rfis = await service.list_by_project(project_id)
    return [RfiRead.model_validate(r, from_attributes=True) for r in rfis]


@router.post(
    "/projects/{project_id}/rfis",
    response_model=RfiRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать RFI",
)
async def create_rfi(
    project_id: UUID,
    payload: RfiCreate,
    service: RfiServiceDep,
) -> RfiRead:
    try:
        task = await service.create(
            project_id=project_id,
            title=payload.title,
            rfi_cause_decision_id=payload.rfi_cause_decision_id,
            rfi_cause_goal_id=payload.rfi_cause_goal_id,
            rfi_due_date=payload.rfi_due_date,
            rfi_state=payload.rfi_state or RfiState.OPEN,
            deadline=payload.deadline,
            assignee_id=payload.assignee_id,
            is_complex=payload.is_complex,
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="conflict"
        ) from err
    return RfiRead.model_validate(task, from_attributes=True)


@router.get(
    "/rfis/{rfi_id}",
    response_model=RfiRead,
    summary="RFI по ID",
)
async def get_rfi(
    rfi_id: UUID,
    service: RfiServiceDep,
) -> RfiRead:
    task = await service.get(rfi_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RFI {rfi_id} not found",
        )
    return RfiRead.model_validate(task, from_attributes=True)


@router.patch(
    "/rfis/{rfi_id}",
    response_model=RfiRead,
    summary="Обновить RFI",
)
async def update_rfi(
    rfi_id: UUID,
    payload: RfiUpdate,
    service: RfiServiceDep,
) -> RfiRead:
    data = payload.model_dump(exclude_unset=True, by_alias=False)
    try:
        task = await service.update(rfi_id, **data)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="conflict"
        ) from err
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RFI {rfi_id} not found",
        )
    return RfiRead.model_validate(task, from_attributes=True)


@router.delete(
    "/rfis/{rfi_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить RFI",
)
async def delete_rfi(
    rfi_id: UUID,
    service: RfiServiceDep,
) -> None:
    try:
        await service.delete(rfi_id)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err


@router.post(
    "/rfis/{rfi_id}/escalate",
    response_model=RfiRead,
    summary="Эскалировать RFI",
)
async def escalate_rfi(
    rfi_id: UUID,
    service: RfiServiceDep,
) -> RfiRead:
    try:
        task = await service.escalate(rfi_id)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    return RfiRead.model_validate(task, from_attributes=True)
