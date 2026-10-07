"""DTO для импорта Excel (ImportLog)."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.src.domain.value_objects.enums import ImportStatus


class ImportPreview(BaseModel):
    """Превью первых строк Excel для маппинга."""

    filename: str
    columns: list[str]
    rows: list[dict]
    total_rows: int = Field(ge=0)


class ColumnMapping(BaseModel):
    """Маппинг колонок Excel → поля задачи."""

    task_title: str = Field(..., description="Колонка с названием задачи")
    description: str | None = None
    deadline: str | None = None
    section: str | None = None
    assignee: str | None = None


class ImportConfirm(BaseModel):
    """Подтверждение маппинга."""

    column_mapping: ColumnMapping


class ImportLogRead(BaseModel):
    """Лог импорта (GET /api/projects/{id}/import-logs)."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    filename: str | None
    rows_imported: int
    rows_failed: int
    status: ImportStatus
    column_mapping: dict | None
    error_details: dict | None
    imported_at: datetime