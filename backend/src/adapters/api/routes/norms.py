"""Роуты для нормативных документов (Norm).

POST   /api/projects/{id}/norms   — создать норму
GET    /api/projects/{id}/norms   — список норм проекта
GET    /api/norms/{id}            — норма по ID
PATCH  /api/norms/{id}            — обновить норму
DELETE /api/norms/{id}            — удалить норму
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from backend.src.adapters.api.dependencies import NormServiceDep
from backend.src.application.dto.norm import (
    NormCreate,
    NormRead,
    NormUpdate,
)

router = APIRouter(prefix="/api", tags=["norms"])


@router.post(
    "/projects/{project_id}/norms",
    response_model=NormRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать норму в проекте",
)
async def create_norm(
    project_id: UUID,
    payload: NormCreate,
    service: NormServiceDep,
) -> NormRead:
    try:
        created = await service.create(
            project_id=project_id,
            code=payload.code,
            title=payload.title,
            norm_type=payload.norm_type,
            issued_at=payload.issued_at,
            source_url=payload.source_url,
            document_id=payload.document_id,
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    except IntegrityError as err:
        # uq_norms_project_code — если валидация сервиса пропустила дубль
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="conflict"
        ) from err
    return NormRead.model_validate(created, from_attributes=True)


@router.get(
    "/projects/{project_id}/norms",
    response_model=list[NormRead],
    summary="Список норм проекта",
)
async def list_norms(
    project_id: UUID,
    service: NormServiceDep,
) -> list[NormRead]:
    norms = await service.list_by_project(project_id)
    return [NormRead.model_validate(n, from_attributes=True) for n in norms]


@router.get(
    "/norms/{norm_id}",
    response_model=NormRead,
    summary="Норма по ID",
)
async def get_norm(
    norm_id: UUID,
    service: NormServiceDep,
) -> NormRead:
    norm = await service.get(norm_id)
    if norm is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Norm {norm_id} not found",
        )
    return NormRead.model_validate(norm, from_attributes=True)


@router.patch(
    "/norms/{norm_id}",
    response_model=NormRead,
    summary="Обновить норму",
)
async def update_norm(
    norm_id: UUID,
    payload: NormUpdate,
    service: NormServiceDep,
) -> NormRead:
    data = payload.model_dump(exclude_unset=True, by_alias=False)
    try:
        updated = await service.update(norm_id, **data)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Norm {norm_id} not found",
        )
    return NormRead.model_validate(updated, from_attributes=True)


@router.delete(
    "/norms/{norm_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить норму",
)
async def delete_norm(
    norm_id: UUID,
    service: NormServiceDep,
) -> None:
    try:
        await service.delete(norm_id)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
