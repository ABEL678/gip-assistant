"""Роуты для ревизий, изменений, решений и стоп-сигналов (§7.2).

POST   /api/documents/{id}/revisions             — создать ревизию
GET    /api/documents/{id}/revisions             — список ревизий документа
GET    /api/revisions/{id}                       — ревизия по ID
POST   /api/revisions/{id}/changes               — создать изменение
GET    /api/revisions/{id}/changes               — список изменений ревизии
POST   /api/changes/{id}/decision                — создать решение по изменению
POST   /api/revisions/{id}/stop-flags            — создать стоп-сигнал
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from backend.src.adapters.api.dependencies import (
    ChangeServiceDep,
    RevisionDecisionServiceDep,
    RevisionServiceDep,
    StopFlagServiceDep,
)
from backend.src.application.dto.change import (
    ChangeCreate,
    ChangeRead,
)
from backend.src.application.dto.revision import (
    RevisionCreate,
    RevisionRead,
)
from backend.src.application.dto.revision_decision import (
    RevisionDecisionCreate,
    RevisionDecisionRead,
)
from backend.src.application.dto.stop_flag import (
    StopFlagCreate,
    StopFlagRead,
)
from backend.src.domain.value_objects.enums import ChangeStatus, RevisionDecisionType

router = APIRouter(prefix="/api", tags=["revisions"])


# ---------- Revisions ----------


@router.post(
    "/documents/{document_id}/revisions",
    response_model=RevisionRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать ревизию документа",
)
async def create_revision(
    document_id: UUID,
    payload: RevisionCreate,
    service: RevisionServiceDep,
) -> RevisionRead:
    try:
        created = await service.create(
            document_id=document_id,
            version=payload.version,
            date=payload.date,
            source=payload.source,
            notified=payload.notified,
            stop_flag=payload.stop_flag,
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    return RevisionRead.model_validate(created, from_attributes=True)


@router.get(
    "/documents/{document_id}/revisions",
    response_model=list[RevisionRead],
    summary="Список ревизий документа",
)
async def list_revisions(
    document_id: UUID,
    service: RevisionServiceDep,
) -> list[RevisionRead]:
    revisions = await service.list_by_document(document_id)
    return [
        RevisionRead.model_validate(r, from_attributes=True) for r in revisions
    ]


@router.get(
    "/revisions/{revision_id}",
    response_model=RevisionRead,
    summary="Ревизия по ID",
)
async def get_revision(
    revision_id: UUID,
    service: RevisionServiceDep,
) -> RevisionRead:
    revision = await service.get_by_id(revision_id)
    if revision is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Revision {revision_id} not found",
        )
    return RevisionRead.model_validate(revision, from_attributes=True)


# ---------- Changes ----------


@router.post(
    "/revisions/{revision_id}/changes",
    response_model=ChangeRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать изменение в ревизии",
)
async def create_change(
    revision_id: UUID,
    payload: ChangeCreate,
    service: ChangeServiceDep,
) -> ChangeRead:
    try:
        created = await service.create(
            revision_id=revision_id,
            field=payload.field,
            status=ChangeStatus(payload.status),
            old_value=payload.old_value,
            new_value=payload.new_value,
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    return ChangeRead.model_validate(created, from_attributes=True)


@router.get(
    "/revisions/{revision_id}/changes",
    response_model=list[ChangeRead],
    summary="Список изменений ревизии",
)
async def list_changes(
    revision_id: UUID,
    service: ChangeServiceDep,
) -> list[ChangeRead]:
    changes = await service.list_by_revision(revision_id)
    return [ChangeRead.model_validate(c, from_attributes=True) for c in changes]


# ---------- Decisions ----------


@router.post(
    "/changes/{change_id}/decision",
    response_model=RevisionDecisionRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать решение по изменению",
)
async def create_decision(
    change_id: UUID,
    payload: RevisionDecisionCreate,
    service: RevisionDecisionServiceDep,
) -> RevisionDecisionRead:
    created = await service.create(
        change_id=change_id,
        decision=RevisionDecisionType(payload.decision),
        decided_by=payload.decided_by,
        deadline=payload.deadline,
    )
    return RevisionDecisionRead.model_validate(created, from_attributes=True)


# ---------- Stop Flags ----------


@router.post(
    "/revisions/{revision_id}/stop-flags",
    response_model=StopFlagRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать стоп-сигнал для ревизии",
)
async def create_stop_flag(
    revision_id: UUID,
    payload: StopFlagCreate,
    service: StopFlagServiceDep,
) -> StopFlagRead:
    try:
        created = await service.create(
            revision_id=revision_id,
            reason=payload.reason,
            resolved=payload.resolved,
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    return StopFlagRead.model_validate(created, from_attributes=True)
