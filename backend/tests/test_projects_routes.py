"""Тест роута POST /api/projects (6.14a: data_security_level)."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from backend.src.adapters.api.dependencies import get_project_repo
from backend.src.adapters.api.routes.projects import router
from backend.src.domain.entities.project import Project
from backend.src.domain.value_objects.enums import DataSecurityLevel


@pytest.mark.asyncio
async def test_create_project_with_red_security_level():
    """POST /api/projects передаёт data_security_level в домен и ответ."""
    repo = AsyncMock()

    async def _save(project: Project) -> Project:
        project.id = project.id or uuid4()
        project.created_at = datetime.now(UTC)
        project.updated_at = datetime.now(UTC)
        return project

    repo.save.side_effect = _save

    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_project_repo] = lambda: repo

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/projects",
            json={
                "name": "Test Project",
                "code": "TEST-RED",
                "data_security_level": "red",
            },
        )

    assert response.status_code == 201
    assert response.json()["data_security_level"] == "red"

    saved = repo.save.call_args.args[0]
    assert saved.data_security_level is DataSecurityLevel.RED
