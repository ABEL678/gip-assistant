"""Роуты для стандартов проекта (ProjectStandard).

POST   /api/premises/{id}/standards              — создать стандарт
GET    /api/premises/{id}/standards              — список стандартов вводной
GET    /api/standards/{id}                       — стандарт по ID
PATCH  /api/standards/{id}                       — обновить стандарт
DELETE /api/standards/{id}                       — удалить стандарт
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from backend.src.adapters.api.dependencies import ProjectStandardServiceDep
from backend.src.application.dto.project_standard import (
    ProjectStandardCreate,
    ProjectStandardRead,
    ProjectStandardUpdate,
)

router = APIRouter(prefix="/api", tags=["project_standards"])


@router.post(
    "/premises/{premise_id}/standards",
    response_model=ProjectStandardRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать стандарт для вводной",
)
async def create_standard(
    premise_id: UUID,
    payload: ProjectStandardCreate,
    service: ProjectStandardServiceDep,
) -> ProjectStandardRead:
    created = await service.create(
        premise_id=premise_id,
        type=payload.type,
        value=payload.value,
    )
    return ProjectStandardRead.model_validate(created, from_attributes=True)


@router.get(
    "/premises/{premise_id}/standards",
    response_model=list[ProjectStandardRead],
    summary="Список стандартов вводной",
)
async def list_standards(
    premise_id: UUID,
    service: ProjectStandardServiceDep,
) -> list[ProjectStandardRead]:
    standards = await service.list_by_premise(premise_id)
    return [
        ProjectStandardRead.model_validate(s, from_attributes=True) for s in standards
    ]


@router.get(
    "/standards/{standard_id}",
    response_model=ProjectStandardRead,
    summary="Стандарт по ID",
)
async def get_standard(
    standard_id: UUID,
    service: ProjectStandardServiceDep,
) -> ProjectStandardRead:
    standard = await service.get_by_id(standard_id)
    if standard is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ProjectStandard {standard_id} not found",
        )
    return ProjectStandardRead.model_validate(standard, from_attributes=True)


@router.patch(
    "/standards/{standard_id}",
    response_model=ProjectStandardRead,
    summary="Обновить стандарт",
)
async def update_standard(
    standard_id: UUID,
    payload: ProjectStandardUpdate,
    service: ProjectStandardServiceDep,
) -> ProjectStandardRead:
    data = payload.model_dump(exclude_unset=True, by_alias=False)
    try:
        updated = await service.update(standard_id, **data)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ProjectStandard {standard_id} not found",
        )
    return ProjectStandardRead.model_validate(updated, from_attributes=True)


@router.delete(
    "/standards/{standard_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить стандарт",
)
async def delete_standard(
    standard_id: UUID,
    service: ProjectStandardServiceDep,
) -> None:
    try:
        await service.delete(standard_id)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
