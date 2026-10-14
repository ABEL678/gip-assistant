"""Роуты для типов ГОСТ-документов.

POST   /api/document-types                  — создать тип
GET    /api/document-types                  — список типов
GET    /api/document-types/by-code/{code}   — тип по коду
GET    /api/document-types/{id}             — тип по ID
PATCH  /api/document-types/{id}             — обновить тип
DELETE /api/document-types/{id}             — удалить тип
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from backend.src.adapters.api.dependencies import DocumentTypeServiceDep
from backend.src.application.dto.document_type import (
    DocumentTypeCreate,
    DocumentTypeRead,
    DocumentTypeUpdate,
)

router = APIRouter(prefix="/api", tags=["document-types"])


# ---------- Document Types ----------


@router.post(
    "/document-types",
    response_model=DocumentTypeRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать тип ГОСТ-документа",
)
async def create_document_type(
    payload: DocumentTypeCreate,
    service: DocumentTypeServiceDep,
) -> DocumentTypeRead:
    created = await service.create(
        code=payload.code,
        name=payload.name,
        description=payload.description,
        gost_code=payload.gost_code,
    )
    return DocumentTypeRead.model_validate(created, from_attributes=True)


@router.get(
    "/document-types",
    response_model=list[DocumentTypeRead],
    summary="Список типов ГОСТ-документов",
)
async def list_document_types(
    service: DocumentTypeServiceDep,
) -> list[DocumentTypeRead]:
    types = await service.list_all()
    return [DocumentTypeRead.model_validate(t, from_attributes=True) for t in types]


@router.get(
    "/document-types/by-code/{code}",
    response_model=DocumentTypeRead,
    summary="Тип ГОСТ-документа по коду",
)
async def get_document_type_by_code(
    code: str,
    service: DocumentTypeServiceDep,
) -> DocumentTypeRead:
    document_type = await service.get_by_code(code)
    if document_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DocumentType with code '{code}' not found",
        )
    return DocumentTypeRead.model_validate(document_type, from_attributes=True)


@router.get(
    "/document-types/{document_type_id}",
    response_model=DocumentTypeRead,
    summary="Тип ГОСТ-документа по ID",
)
async def get_document_type(
    document_type_id: UUID,
    service: DocumentTypeServiceDep,
) -> DocumentTypeRead:
    document_type = await service.get_by_id(document_type_id)
    if document_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DocumentType {document_type_id} not found",
        )
    return DocumentTypeRead.model_validate(document_type, from_attributes=True)


@router.patch(
    "/document-types/{document_type_id}",
    response_model=DocumentTypeRead,
    summary="Обновить тип ГОСТ-документа",
)
async def update_document_type(
    document_type_id: UUID,
    payload: DocumentTypeUpdate,
    service: DocumentTypeServiceDep,
) -> DocumentTypeRead:
    data = payload.model_dump(exclude_unset=True, by_alias=False)
    updated = await service.update(
        document_type_id,
        name=data.get("name"),
        description=data.get("description"),
        gost_code=data.get("gost_code"),
    )
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DocumentType {document_type_id} not found",
        )
    return DocumentTypeRead.model_validate(updated, from_attributes=True)


@router.delete(
    "/document-types/{document_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить тип ГОСТ-документа",
)
async def delete_document_type(
    document_type_id: UUID,
    service: DocumentTypeServiceDep,
) -> None:
    try:
        deleted = await service.delete(document_type_id)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DocumentType {document_type_id} not found",
        )
