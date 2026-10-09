"""Роуты для проектов.

POST /api/projects          — создать проект
GET  /api/projects          — список проектов
GET  /api/projects/{id}     — проект по ID
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from backend.src.adapters.api.dependencies import ProjectRepoDep
from backend.src.application.dto.project import (
    ProjectCreate,
    ProjectRead,
)
from backend.src.domain.entities.project import Project

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post(
    "",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать проект",
)
async def create_project(
    payload: ProjectCreate,
    repo: ProjectRepoDep,
) -> ProjectRead:
    project = Project(
        name=payload.name,
        code=payload.code,
        stage=payload.stage,
        client=payload.client,
        contract_number=payload.contract_number,
    )
    saved = await repo.save(project)
    return ProjectRead.model_validate(saved, from_attributes=True)


@router.get(
    "",
    response_model=list[ProjectRead],
    summary="Список проектов",
)
async def list_projects(
    repo: ProjectRepoDep,
    limit: int = 100,
    offset: int = 0,
) -> list[ProjectRead]:
    projects = await repo.get_all(limit=limit, offset=offset)
    return [ProjectRead.model_validate(p, from_attributes=True) for p in projects]


@router.get(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Проект по ID",
)
async def get_project(
    project_id: UUID,
    repo: ProjectRepoDep,
) -> ProjectRead:
    project = await repo.get_by_id(project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found",
        )
    return ProjectRead.model_validate(project, from_attributes=True)
