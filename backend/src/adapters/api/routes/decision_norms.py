"""Роуты для связи Decision ↔ Norm (decision_norms, M:N).

POST   /api/decisions/{id}/norms/{norm_id}  — связать решение с нормой
DELETE /api/decisions/{id}/norms/{norm_id}  — разорвать связь
GET    /api/decisions/{id}/norms            — UUID норм решения
GET    /api/norms/{id}/decisions            — UUID решений нормы
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from backend.src.adapters.api.dependencies import DecisionNormServiceDep

router = APIRouter(prefix="/api", tags=["decision-norms"])


@router.post(
    "/decisions/{decision_id}/norms/{norm_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Связать решение с нормой",
)
async def link_decision_norm(
    decision_id: UUID,
    norm_id: UUID,
    service: DecisionNormServiceDep,
) -> None:
    try:
        await service.link(decision_id, norm_id)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err


@router.delete(
    "/decisions/{decision_id}/norms/{norm_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Разорвать связь решения с нормой",
)
async def unlink_decision_norm(
    decision_id: UUID,
    norm_id: UUID,
    service: DecisionNormServiceDep,
) -> None:
    await service.unlink(decision_id, norm_id)


@router.get(
    "/decisions/{decision_id}/norms",
    response_model=list[UUID],
    summary="UUID норм, связанных с решением",
)
async def list_norms_by_decision(
    decision_id: UUID,
    service: DecisionNormServiceDep,
) -> list[UUID]:
    return await service.list_norms_by_decision(decision_id)


@router.get(
    "/norms/{norm_id}/decisions",
    response_model=list[UUID],
    summary="UUID решений, связанных с нормой",
)
async def list_decisions_by_norm(
    norm_id: UUID,
    service: DecisionNormServiceDep,
) -> list[UUID]:
    return await service.list_decisions_by_norm(norm_id)
