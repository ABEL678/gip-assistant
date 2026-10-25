"""Роуты для ГОСТ-документов.

POST   /api/projects/{id}/documents                 — создать документ
GET    /api/projects/{id}/documents                 — список документов проекта
GET    /api/documents/by-guid/{guid}                — документ по GUID
GET    /api/documents/{id}                          — документ по ID
PATCH  /api/documents/{id}                          — обновить документ
DELETE /api/documents/{id}                          — удалить документ
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from backend.src.adapters.api.dependencies import DocumentServiceDep
from backend.src.application.dto.document import (
    DocumentCreate,
    DocumentRead,
    DocumentUpdate,
)
from backend.src.domain.value_objects.document import LifecycleStatus

router = APIRouter(prefix="/api", tags=["documents"])


# ---------- Documents ----------


@router.post(
    "/projects/{project_id}/documents",
    response_model=DocumentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать ГОСТ-документ в проекте",
)
async def create_document(
    project_id: UUID,
    payload: DocumentCreate,
    service: DocumentServiceDep,
) -> DocumentRead:
    try:
        created = await service.create(
            project_id=project_id,
            document_type_id=payload.document_type_id,
            document_name=payload.document_name,
            cipher=payload.cipher,
            document_kind=payload.document_kind,
            doc_part_type=payload.doc_part_type,
            section_code=payload.section_code,
            mark=payload.mark,
            base_designation=payload.base_designation,
            entity_id=payload.entity_id,
            task_id=payload.task_id,
            lifecycle_status=payload.lifecycle_status,
            version_parent_id=payload.version_parent_id,
            replaces_id=payload.replaces_id,
            replaced_by_id=payload.replaced_by_id,
            rfi_id=payload.rfi_id,
            trigger_action_id=payload.trigger_action_id,
        )
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err
    return DocumentRead.model_validate(created, from_attributes=True)


@router.get(
    "/projects/{project_id}/documents",
    response_model=list[DocumentRead],
    summary="Список документов проекта",
)
async def list_documents(
    project_id: UUID,
    service: DocumentServiceDep,
    lifecycle_status: LifecycleStatus | None = Query(
        None, description="Фильтр по статусу"
    ),
) -> list[DocumentRead]:
    docs = await service.list_by_project(project_id, lifecycle_status=lifecycle_status)
    return [DocumentRead.model_validate(d, from_attributes=True) for d in docs]


@router.get(
    "/documents/by-guid/{guid}",
    response_model=DocumentRead,
    summary="ГОСТ-документ по GUID",
)
async def get_document_by_guid(
    guid: UUID,
    service: DocumentServiceDep,
) -> DocumentRead:
    # ВАЖНО: by-guid объявлен раньше {document_id} — иначе конфликт
    document = await service.get_by_guid(guid)
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with guid {guid} not found",
        )
    return DocumentRead.model_validate(document, from_attributes=True)


@router.get(
    "/documents/{document_id}",
    response_model=DocumentRead,
    summary="ГОСТ-документ по ID",
)
async def get_document(
    document_id: UUID,
    service: DocumentServiceDep,
) -> DocumentRead:
    document = await service.get_by_id(document_id)
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document {document_id} not found",
        )
    return DocumentRead.model_validate(document, from_attributes=True)


@router.patch(
    "/documents/{document_id}",
    response_model=DocumentRead,
    summary="Обновить ГОСТ-документ",
)
async def update_document(
    document_id: UUID,
    payload: DocumentUpdate,
    service: DocumentServiceDep,
) -> DocumentRead:
    data = payload.model_dump(exclude_unset=True, by_alias=False)
    try:
        updated = await service.update(
            document_id,
            document_name=data.get("document_name"),
            document_kind=data.get("document_kind"),
            doc_part_type=data.get("doc_part_type"),
            section_code=data.get("section_code"),
            mark=data.get("mark"),
            base_designation=data.get("base_designation"),
            lifecycle_status=data.get("lifecycle_status"),
            rfi_id=data.get("rfi_id"),
            trigger_action_id=data.get("trigger_action_id"),
        )
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document {document_id} not found",
        )
    return DocumentRead.model_validate(updated, from_attributes=True)


@router.delete(
    "/documents/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить ГОСТ-документ",
)
async def delete_document(
    document_id: UUID,
    service: DocumentServiceDep,
) -> None:
    try:
        deleted = await service.delete(document_id)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document {document_id} not found",
        )
