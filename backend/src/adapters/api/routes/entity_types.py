"""Роуты универсальных сущностей (EntityType + Entity).

POST   /api/projects/{id}/entity-types             — создать тип
GET    /api/projects/{id}/entity-types             — список типов проекта
GET    /api/entity-types/{id}                       — тип по ID
PATCH  /api/entity-types/{id}                       — обновить тип
DELETE /api/entity-types/{id}                       — удалить тип

POST   /api/entity-types/{id}/entities              — создать запись
GET    /api/entity-types/{id}/entities              — список записей типа
GET    /api/entities/{id}                           — запись по ID
PATCH  /api/entities/{id}                           — обновить запись
DELETE /api/entities/{id}                           — удалить запись
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from backend.src.adapters.api.dependencies import (
    EntityRepoDep,
    EntityServiceDep,
    EntityTypeRepoDep,
    EntityTypeServiceDep,
)
from backend.src.application.dto.entity import (
    EntityCreate,
    EntityRead,
    EntityUpdate,
)
from backend.src.application.dto.entity_type import (
    EntityTypeCreate,
    EntityTypeRead,
    EntityTypeUpdate,
)

router = APIRouter(prefix="/api", tags=["entity-types"])


# ---------- EntityType ----------


@router.post(
    "/projects/{project_id}/entity-types",
    response_model=EntityTypeRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать тип сущности в проекте",
)
async def create_entity_type(
    project_id: UUID,
    payload: EntityTypeCreate,
    service: EntityTypeServiceDep,
) -> EntityTypeRead:
    try:
        created = await service.create(
            project_id=project_id,
            name=payload.name,
            icon=payload.icon,
            color=payload.color,
            description=payload.description,
            field_schema=payload.schema_.model_dump(mode="json"),
            sort_order=payload.sort_order,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return EntityTypeRead.model_validate(created, from_attributes=True)


@router.get(
    "/projects/{project_id}/entity-types",
    response_model=list[EntityTypeRead],
    summary="Список типов сущностей проекта",
)
async def list_entity_types(
    project_id: UUID,
    service: EntityTypeServiceDep,
) -> list[EntityTypeRead]:
    types = await service.list_by_project(project_id)
    return [
        EntityTypeRead.model_validate(t, from_attributes=True) for t in types
    ]


@router.get(
    "/entity-types/{entity_type_id}",
    response_model=EntityTypeRead,
    summary="Тип сущности по ID",
)
async def get_entity_type(
    entity_type_id: UUID,
    service: EntityTypeServiceDep,
) -> EntityTypeRead:
    entity_type = await service.get_by_id(entity_type_id)
    if entity_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"EntityType {entity_type_id} not found",
        )
    return EntityTypeRead.model_validate(entity_type, from_attributes=True)


@router.patch(
    "/entity-types/{entity_type_id}",
    response_model=EntityTypeRead,
    summary="Обновить тип сущности",
)
async def update_entity_type(
    entity_type_id: UUID,
    payload: EntityTypeUpdate,
    service: EntityTypeServiceDep,
) -> EntityTypeRead:
    data = payload.model_dump(exclude_unset=True, by_alias=False)
    field_schema_dto = data.pop("schema_", None)
    field_schema = (
        field_schema_dto.model_dump(mode="json")
        if field_schema_dto is not None
        else None
    )

    updated = await service.update(
        entity_type_id,
        name=data.get("name"),
        icon=data.get("icon"),
        color=data.get("color"),
        description=data.get("description"),
        field_schema=field_schema,
        sort_order=data.get("sort_order"),
    )
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"EntityType {entity_type_id} not found",
        )
    return EntityTypeRead.model_validate(updated, from_attributes=True)


@router.delete(
    "/entity-types/{entity_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить тип сущности",
)
async def delete_entity_type(
    entity_type_id: UUID,
    service: EntityTypeServiceDep,
) -> None:
    try:
        deleted = await service.delete(entity_type_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"EntityType {entity_type_id} not found",
        )


# ---------- Entity ----------


@router.post(
    "/entity-types/{entity_type_id}/entities",
    response_model=EntityRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать запись в типе сущности",
)
async def create_entity(
    entity_type_id: UUID,
    payload: EntityCreate,
    service: EntityServiceDep,
) -> EntityRead:
    try:
        created = await service.create(
            project_id=payload.project_id,
            entity_type_id=entity_type_id,
            data=payload.data,
            sort_order=payload.sort_order,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return EntityRead.model_validate(created, from_attributes=True)


@router.get(
    "/entity-types/{entity_type_id}/entities",
    response_model=list[EntityRead],
    summary="Список записей типа сущности",
)
async def list_entities(
    entity_type_id: UUID,
    service: EntityServiceDep,
) -> list[EntityRead]:
    entities = await service.list_by_type(entity_type_id)
    return [EntityRead.model_validate(e, from_attributes=True) for e in entities]


@router.get(
    "/entities/{entity_id}",
    response_model=EntityRead,
    summary="Запись по ID",
)
async def get_entity(
    entity_id: UUID,
    service: EntityServiceDep,
) -> EntityRead:
    entity = await service.get_by_id(entity_id)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entity {entity_id} not found",
        )
    return EntityRead.model_validate(entity, from_attributes=True)


@router.patch(
    "/entities/{entity_id}",
    response_model=EntityRead,
    summary="Обновить запись",
)
async def update_entity(
    entity_id: UUID,
    payload: EntityUpdate,
    service: EntityServiceDep,
) -> EntityRead:
    data = payload.model_dump(exclude_unset=True)
    try:
        updated = await service.update(
            entity_id,
            data=data.get("data"),
            sort_order=data.get("sort_order"),
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entity {entity_id} not found",
        )
    return EntityRead.model_validate(updated, from_attributes=True)


@router.delete(
    "/entities/{entity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить запись",
)
async def delete_entity(
    entity_id: UUID,
    service: EntityServiceDep,
) -> None:
    deleted = await service.delete(entity_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entity {entity_id} not found",
        )