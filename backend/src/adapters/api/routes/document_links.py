"""Роуты для связей ГОСТ-документов.

POST   /api/documents/{id}/links          — создать связь
GET    /api/documents/{id}/links          — исходящие связи
GET    /api/documents/{id}/links/incoming — входящие связи
DELETE /api/document-links/{id}           — удалить связь
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from backend.src.adapters.api.dependencies import DocumentLinkServiceDep
from backend.src.application.dto.document_link import (
    DocumentLinkCreate,
    DocumentLinkRead,
)

router = APIRouter(prefix="/api", tags=["document-links"])


# ---------- Document Links ----------


@router.post(
    "/documents/{document_id}/links",
    response_model=DocumentLinkRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать связь ГОСТ-документов",
)
async def create_document_link(
    document_id: UUID,
    payload: DocumentLinkCreate,
    service: DocumentLinkServiceDep,
) -> DocumentLinkRead:
    # source_document_id из URL, payload.source_document_id игнорируется
    try:
        created = await service.create(
            source_document_id=document_id,
            target_document_id=payload.target_document_id,
            link_type=payload.link_type,
        )
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err
    return DocumentLinkRead.model_validate(created, from_attributes=True)


@router.get(
    "/documents/{document_id}/links",
    response_model=list[DocumentLinkRead],
    summary="Исходящие связи ГОСТ-документа",
)
async def list_document_links(
    document_id: UUID,
    service: DocumentLinkServiceDep,
) -> list[DocumentLinkRead]:
    links = await service.list_by_source(document_id)
    return [
        DocumentLinkRead.model_validate(link, from_attributes=True) for link in links
    ]


@router.get(
    "/documents/{document_id}/links/incoming",
    response_model=list[DocumentLinkRead],
    summary="Входящие связи ГОСТ-документа",
)
async def list_incoming_document_links(
    document_id: UUID,
    service: DocumentLinkServiceDep,
) -> list[DocumentLinkRead]:
    links = await service.list_by_target(document_id)
    return [
        DocumentLinkRead.model_validate(link, from_attributes=True) for link in links
    ]


@router.delete(
    "/document-links/{link_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить связь ГОСТ-документов",
)
async def delete_document_link(
    link_id: UUID,
    service: DocumentLinkServiceDep,
) -> None:
    try:
        deleted = await service.delete(link_id)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DocumentLink {link_id} not found",
        )
