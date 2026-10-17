"""Роуты для вводных (Premise).

POST   /api/projects/{id}/premises                — создать вводную
GET    /api/projects/{id}/premises                — список вводных проекта
GET    /api/premises/{id}                         — вводная по ID
PATCH  /api/premises/{id}                         — обновить вводную
DELETE /api/premises/{id}                         — удалить вводную
"""

from uuid import UUID

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from backend.src.adapters.api.dependencies import PremiseServiceDep
from backend.src.application.dto.premise import (
    PremiseCreate,
    PremiseRead,
    PremiseUpdate,
)
from backend.src.domain.value_objects.enums import PremiseCategory
import os
import uuid
from pathlib import Path

UPLOAD_DIR = Path("backend/uploads")

router = APIRouter(prefix="/api", tags=["premises"])


@router.post(
    "/projects/{project_id}/premises",
    response_model=PremiseRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать вводную в проекте",
)
async def create_premise(
    project_id: UUID,
    payload: PremiseCreate,
    service: PremiseServiceDep,
) -> PremiseRead:
    try:
        created = await service.create(
            project_id=project_id,
            category=payload.category,
            name=payload.name,
            source=payload.source,
            date=payload.date,
            actual=payload.actual,
            mandatory=payload.mandatory,
            link=payload.link,
            valid_until=payload.valid_until,
            data=payload.data,
            schema=payload.schema_,
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    return PremiseRead.model_validate(created, from_attributes=True)


@router.get(
    "/projects/{project_id}/premises",
    response_model=list[PremiseRead],
    summary="Список вводных проекта",
)
async def list_premises(
    project_id: UUID,
    service: PremiseServiceDep,
) -> list[PremiseRead]:
    premises = await service.list_by_project(project_id)
    return [PremiseRead.model_validate(p, from_attributes=True) for p in premises]


@router.get(
    "/premises/{premise_id}",
    response_model=PremiseRead,
    summary="Вводная по ID",
)
async def get_premise(
    premise_id: UUID,
    service: PremiseServiceDep,
) -> PremiseRead:
    premise = await service.get(premise_id)
    if premise is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Premise {premise_id} not found",
        )
    return PremiseRead.model_validate(premise, from_attributes=True)


@router.patch(
    "/premises/{premise_id}",
    response_model=PremiseRead,
    summary="Обновить вводную",
)
async def update_premise(
    premise_id: UUID,
    payload: PremiseUpdate,
    service: PremiseServiceDep,
) -> PremiseRead:
    data = payload.model_dump(exclude_unset=True, by_alias=False)
    # Преобразуем schema_ обратно в schema для сервиса
    if "schema_" in data:
        data["schema"] = data.pop("schema_")
    try:
        updated = await service.update(premise_id, **data)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Premise {premise_id} not found",
        )
    return PremiseRead.model_validate(updated, from_attributes=True)


@router.delete(
    "/premises/{premise_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить вводную",
)
async def delete_premise(
    premise_id: UUID,
    service: PremiseServiceDep,
) -> None:
    try:
        await service.delete(premise_id)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err


@router.post(
    "/projects/{project_id}/premises/upload",
    response_model=PremiseRead,
    status_code=status.HTTP_201_CREATED,
    summary="Загрузить файл-исходник",
)
async def upload_premise_file(
    project_id: UUID,
    file: UploadFile = File(...),
    category: PremiseCategory = Form(PremiseCategory.SOURCE_DATA),
    name: str | None = Form(None),
    service: PremiseServiceDep = None,  # type: ignore[assignment]
) -> PremiseRead:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    project_dir = UPLOAD_DIR / str(project_id)
    project_dir.mkdir(exist_ok=True)

    file_id = uuid.uuid4()
    safe_name = file.filename or "file"
    file_path = project_dir / f"{file_id}_{safe_name}"

    content = await file.read()
    if len(content) > 50 * 1024 * 1024:
        raise HTTPException(400, "File too large (max 50 MB)")

    with open(file_path, "wb") as f:
        f.write(content)

    premise_name = name or Path(safe_name).stem
    data = {
        "file_path": str(file_path),
        "file_name": safe_name,
        "file_size": len(content),
        "mime_type": file.content_type,
    }

    created = await service.create(
        project_id=project_id,
        category=category,
        name=premise_name,
        data=data,
    )
    return PremiseRead.model_validate(created, from_attributes=True)


@router.get("/premises/{premise_id}/file")
async def download_premise_file(
    premise_id: UUID,
    service: PremiseServiceDep = None,  # type: ignore[assignment]
):
    premise = await service.get(premise_id)
    if not premise:
        raise HTTPException(404, "Premise not found")
    file_path = premise.data.get("file_path") if premise.data else None
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(404, "File not found")
    return FileResponse(file_path, filename=premise.data.get("file_name"))
