"""Роуты импорта Excel (ТЗ 3.0, раздел 5.1.2).

POST /api/projects/{id}/import-excel     — загрузка файла + превью
POST /api/projects/{id}/import-confirm   — подтверждение маппинга
GET  /api/projects/{id}/import-logs      — история импортов
"""

import json
from uuid import UUID

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
)

from backend.src.adapters.api.dependencies import (
    ImportLogRepoDep,
    ImportServiceDep,
    ProjectRepoDep,
)
from backend.src.adapters.import_export import ExcelParseError, parse_excel
from backend.src.application.dto.import_log import (
    ImportConfirm,
    ImportLogRead,
    ImportPreview,
)

router = APIRouter(prefix="/api/projects", tags=["import"])


@router.post(
    "/{project_id}/import-excel",
    response_model=ImportPreview,
    summary="Загрузить Excel и получить превью",
)
async def import_excel_preview(
    project_id: UUID,
    repo: ProjectRepoDep,
    file: UploadFile = File(..., description="Excel-файл (.xlsx, до 10 MB)"),
    header_row: int | None = Query(
        None,
        ge=0,
        le=100,
        description="Индекс строки заголовков (0-based). "
        "Если не указан — ищется автоматически.",
    ),
) -> ImportPreview:
    """Прочитать Excel, вернуть превью для маппинга."""
    # 1. Проверить, что проект существует
    project = await repo.get_by_id(project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found",
        )

    # 2. Проверить расширение
    if file.filename is None or not file.filename.lower().endswith((".xlsx", ".xlsm")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .xlsx / .xlsm files are supported",
        )

    # 3. Прочитать файл
    contents = await file.read()
    try:
        result = parse_excel(contents, max_rows=3, header_row=header_row)
    except ExcelParseError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # 4. Вернуть превью
    return ImportPreview(
        filename=file.filename,
        columns=result.columns,
        rows=result.rows,
        total_rows=result.total_rows,
        suggested_mapping=result.suggested_mapping,
        header_row_index=result.header_row_index,
        preview_rows_raw=result.preview_rows_raw,
        sheet_name=result.sheet_name,
    )


@router.post(
    "/{project_id}/import-confirm",
    summary="Подтвердить маппинг и создать задачи",
)
async def import_confirm(
    project_id: UUID,
    repo: ProjectRepoDep,
    service: ImportServiceDep,
    payload: str = Form(
        ...,
        description='JSON: {"column_mapping": {"task_title": "...", ...}}',
    ),
    file: UploadFile = File(..., description="Тот же Excel-файл"),
    header_row: int | None = Query(
        None,
        ge=0,
        le=100,
        description="Индекс строки заголовков (0-based). Тот же, что был "
        "при /import-excel.",
    ),
) -> dict:
    """Прочитать файл целиком + применить маппинг → создать задачи."""
    project = await repo.get_by_id(project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found",
        )

    # Парсим payload из JSON-строки
    try:
        payload_data = ImportConfirm.model_validate(json.loads(payload))
    except (json.JSONDecodeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid payload JSON: {exc}",
        ) from exc

    contents = await file.read()
    try:
        result = parse_excel(contents, header_row=header_row)
    except ExcelParseError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    import_result = await service.import_excel(
        project_id=project_id,
        rows=result.rows,
        column_mapping=payload_data.column_mapping.model_dump(exclude_none=True),
        filename=file.filename,
    )

    return {
        "log_id": str(import_result.log_id),
        "tasks_created": import_result.tasks_created,
        "errors": [{"row": e.row, "message": e.message} for e in import_result.errors],
    }


@router.get(
    "/{project_id}/import-logs",
    response_model=list[ImportLogRead],
    summary="История импортов проекта",
)
async def list_import_logs(
    project_id: UUID,
    repo: ImportLogRepoDep,
) -> list[ImportLogRead]:
    logs = await repo.get_by_project(project_id)
    return [ImportLogRead.model_validate(log, from_attributes=True) for log in logs]