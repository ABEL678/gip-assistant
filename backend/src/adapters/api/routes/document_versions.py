"""Роуты для версий ГОСТ-документов.

POST   /api/documents/{id}/versions                              — создать версию
GET    /api/documents/{id}/versions/current                      — текущая версия
GET    /api/documents/{id}/versions                              — список версий
GET    /api/document-versions/{id}                               — версия по ID
PATCH  /api/documents/{id}/versions/{version_id}/set-current     — сделать текущей
DELETE /api/document-versions/{id}                               — удалить версию
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from backend.src.adapters.api.dependencies import DocumentVersionServiceDep
from backend.src.application.dto.document_version import (
    DocumentVersionCreate,
    DocumentVersionRead,
)

router = APIRouter(prefix="/api", tags=["document-versions"])


# ---------- Document Versions ----------


@router.post(
    "/documents/{document_id}/versions",
    response_model=DocumentVersionRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать версию ГОСТ-документа",
)
async def create_document_version(
    document_id: UUID,
    payload: DocumentVersionCreate,
    service: DocumentVersionServiceDep,
) -> DocumentVersionRead:
    try:
        created = await service.create(
            document_id=document_id,
            version=payload.version,
            file_path=payload.file_path,
            file_name=payload.file_name,
            hash_sha256=payload.hash_sha256,
            format_original=payload.format_original,
            size_bytes=payload.size_bytes,
            change_number=payload.change_number,
            format_archive=payload.format_archive,
            uploaded_by=None,
        )
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err
    return DocumentVersionRead.model_validate(created, from_attributes=True)


@router.get(
    "/documents/{document_id}/versions/current",
    response_model=DocumentVersionRead,
    summary="Текущая версия ГОСТ-документа",
)
async def get_current_document_version(
    document_id: UUID,
    service: DocumentVersionServiceDep,
) -> DocumentVersionRead:
    # ВАЖНО: /current объявлен раньше /versions — иначе FastAPI запутается
    version = await service.get_current(document_id)
    if version is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Current version for document {document_id} not found",
        )
    return DocumentVersionRead.model_validate(version, from_attributes=True)


@router.get(
    "/documents/{document_id}/versions",
    response_model=list[DocumentVersionRead],
    summary="Список версий ГОСТ-документа",
)
async def list_document_versions(
    document_id: UUID,
    service: DocumentVersionServiceDep,
) -> list[DocumentVersionRead]:
    versions = await service.list_by_document(document_id)
    return [
        DocumentVersionRead.model_validate(v, from_attributes=True) for v in versions
    ]


@router.get(
    "/document-versions/{version_id}",
    response_model=DocumentVersionRead,
    summary="Версия ГОСТ-документа по ID",
)
async def get_document_version(
    version_id: UUID,
    service: DocumentVersionServiceDep,
) -> DocumentVersionRead:
    version = await service.get_by_id(version_id)
    if version is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DocumentVersion {version_id} not found",
        )
    return DocumentVersionRead.model_validate(version, from_attributes=True)


@router.patch(
    "/documents/{document_id}/versions/{version_id}/set-current",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Сделать версию текущей",
)
async def set_current_document_version(
    document_id: UUID,
    version_id: UUID,
    service: DocumentVersionServiceDep,
) -> None:
    # ВАЖНО: PATCH, не POST — изменение состояния
    try:
        await service.set_current(document_id, version_id)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err


@router.delete(
    "/document-versions/{version_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить версию ГОСТ-документа",
)
async def delete_document_version(
    version_id: UUID,
    service: DocumentVersionServiceDep,
) -> None:
    try:
        deleted = await service.delete(version_id)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DocumentVersion {version_id} not found",
        )
