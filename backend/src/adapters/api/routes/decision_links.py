"""Роуты для связей решений (DecisionLink).

POST   /api/projects/{id}/decision-links   — создать связь
GET    /api/projects/{id}/decision-links   — список связей проекта
GET    /api/decision-links/{id}            — связь по ID
DELETE /api/decision-links/{id}            — удалить связь
GET    /api/decisions/{id}/links           — связи решения (обе стороны)
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from backend.src.adapters.api.dependencies import DecisionLinkServiceDep
from backend.src.application.dto.decision_link import (
    DecisionLinkCreate,
    DecisionLinkRead,
)

router = APIRouter(prefix="/api", tags=["decision-links"])


@router.post(
    "/projects/{project_id}/decision-links",
    response_model=DecisionLinkRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать связь между решениями",
)
async def create_decision_link(
    project_id: UUID,
    payload: DecisionLinkCreate,
    service: DecisionLinkServiceDep,
) -> DecisionLinkRead:
    try:
        created = await service.create(
            project_id=project_id,
            from_decision_id=payload.from_decision_id,
            to_decision_id=payload.to_decision_id,
            link_type=payload.link_type,
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    except IntegrityError as err:
        # uq_decision_links_triple / ck_decision_links_no_self —
        # если валидация сервиса пропустила дубль или self-link
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="conflict"
        ) from err
    return DecisionLinkRead.model_validate(created, from_attributes=True)


@router.get(
    "/projects/{project_id}/decision-links",
    response_model=list[DecisionLinkRead],
    summary="Список связей проекта",
)
async def list_decision_links(
    project_id: UUID,
    service: DecisionLinkServiceDep,
) -> list[DecisionLinkRead]:
    links = await service.list_by_project(project_id)
    return [DecisionLinkRead.model_validate(link, from_attributes=True) for link in links]


@router.get(
    "/decision-links/{link_id}",
    response_model=DecisionLinkRead,
    summary="Связь по ID",
)
async def get_decision_link(
    link_id: UUID,
    service: DecisionLinkServiceDep,
) -> DecisionLinkRead:
    link = await service.get_by_id(link_id)
    if link is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DecisionLink {link_id} not found",
        )
    return DecisionLinkRead.model_validate(link, from_attributes=True)


@router.delete(
    "/decision-links/{link_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить связь",
)
async def delete_decision_link(
    link_id: UUID,
    service: DecisionLinkServiceDep,
) -> None:
    deleted = await service.delete(link_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DecisionLink {link_id} not found",
        )


@router.get(
    "/decisions/{decision_id}/links",
    response_model=list[DecisionLinkRead],
    summary="Связи решения (from и to)",
)
async def list_links_by_decision(
    decision_id: UUID,
    service: DecisionLinkServiceDep,
) -> list[DecisionLinkRead]:
    links = await service.list_by_decision(decision_id)
    return [DecisionLinkRead.model_validate(link, from_attributes=True) for link in links]
