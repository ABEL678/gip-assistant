"""Роуты для результатов проекта (Result).

POST   /api/projects/{id}/results                — создать результат
GET    /api/projects/{id}/results                — список результатов проекта
GET    /api/results/{id}                         — результат по ID
PATCH  /api/results/{id}                         — обновить результат
DELETE /api/results/{id}                         — удалить результат
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from backend.src.adapters.api.dependencies import ResultServiceDep
from backend.src.application.dto.result import (
    ResultCreate,
    ResultRead,
    ResultUpdate,
)

router = APIRouter(prefix="/api", tags=["results"])


@router.post(
    "/projects/{project_id}/results",
    response_model=ResultRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать результат в проекте",
)
async def create_result(
    project_id: UUID,
    payload: ResultCreate,
    service: ResultServiceDep,
) -> ResultRead:
    try:
        created = await service.create(
            project_id=project_id,
            formulation=payload.formulation,
            source=payload.source,
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    return ResultRead.model_validate(created, from_attributes=True)


@router.get(
    "/projects/{project_id}/results",
    response_model=list[ResultRead],
    summary="Список результатов проекта",
)
async def list_results(
    project_id: UUID,
    service: ResultServiceDep,
) -> list[ResultRead]:
    results = await service.list_by_project(project_id)
    return [ResultRead.model_validate(r, from_attributes=True) for r in results]


@router.get(
    "/results/{result_id}",
    response_model=ResultRead,
    summary="Результат по ID",
)
async def get_result(
    result_id: UUID,
    service: ResultServiceDep,
) -> ResultRead:
    result = await service.get_by_id(result_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Result {result_id} not found",
        )
    return ResultRead.model_validate(result, from_attributes=True)


@router.patch(
    "/results/{result_id}",
    response_model=ResultRead,
    summary="Обновить результат",
)
async def update_result(
    result_id: UUID,
    payload: ResultUpdate,
    service: ResultServiceDep,
) -> ResultRead:
    data = payload.model_dump(exclude_unset=True, by_alias=False)
    try:
        updated = await service.update(result_id, **data)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Result {result_id} not found",
        )
    return ResultRead.model_validate(updated, from_attributes=True)


@router.delete(
    "/results/{result_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить результат",
)
async def delete_result(
    result_id: UUID,
    service: ResultServiceDep,
) -> None:
    try:
        await service.delete(result_id)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
