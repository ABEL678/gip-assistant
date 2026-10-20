"""Тесты роутов ProjectStandard (6 тестов).

Используем httpx.AsyncClient + ASGITransport.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from backend.src.domain.value_objects.enums import ProjectStandardType


def _make_standard(
    id: UUID = None,
    premise_id: UUID = None,
    type: ProjectStandardType = ProjectStandardType.DEADLINE,
    value: dict = None,
    approved_by: UUID = None,
    created_at: datetime = None,
    updated_at: datetime = None,
):
    """Создать мок project standard."""
    standard = AsyncMock()
    standard.id = id or uuid4()
    standard.premise_id = premise_id or uuid4()
    standard.type = type
    standard.value = value or {}
    standard.approved_by = approved_by
    standard.created_at = created_at or datetime.now(timezone.utc)
    standard.updated_at = updated_at or datetime.now(timezone.utc)
    return standard


class TestProjectStandardsRoutes:
    """Тесты роутов ProjectStandard."""

    @pytest.fixture
    async def mock_service(self):
        """Мокированный ProjectStandardService."""
        service = AsyncMock()
        service.get_by_id = AsyncMock()
        service.list_by_premise = AsyncMock()
        service.create = AsyncMock()
        service.update = AsyncMock()
        service.delete = AsyncMock()
        return service

    @pytest.fixture
    async def client(self, mock_service):
        """Создаём AsyncClient с моками зависимостей."""
        from backend.src.adapters.api.dependencies import (
            get_project_standard_service,
        )
        from backend.src.adapters.api.routes.project_standards import (
            router as project_standards_router,
        )

        app = FastAPI()
        app.include_router(project_standards_router)

        app.dependency_overrides[get_project_standard_service] = lambda: mock_service

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

        app.dependency_overrides.clear()

    async def test_list_standards(self, client, mock_service):
        """GET /api/premises/{id}/standards — список."""
        premise_id = uuid4()
        standard_obj = _make_standard(
            id=uuid4(),
            type=ProjectStandardType.DEADLINE,
        )
        mock_service.list_by_premise.return_value = [standard_obj]

        response = await client.get(f"/api/premises/{premise_id}/standards")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["type"] == "deadline"

    async def test_create_standard(self, client, mock_service):
        """POST /api/premises/{id}/standards — 201."""
        premise_id = uuid4()
        created = _make_standard(
            id=uuid4(),
            type=ProjectStandardType.COMPOSITION,
            value={"key": "value"},
        )
        mock_service.create.return_value = created

        response = await client.post(
            f"/api/premises/{premise_id}/standards",
            json={
                "premise_id": str(premise_id),
                "type": "composition",
                "value": {"key": "value"},
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["type"] == "composition"
        assert "id" in data

    async def test_get_standard_by_id(self, client, mock_service):
        """GET /api/standards/{id} — 200."""
        standard_id = uuid4()
        standard_obj = _make_standard(id=standard_id)
        mock_service.get_by_id.return_value = standard_obj

        response = await client.get(f"/api/standards/{standard_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(standard_id)

    async def test_get_standard_not_found(self, client, mock_service):
        """GET /api/standards/{nonexistent} — 404."""
        standard_id = uuid4()
        mock_service.get_by_id.return_value = None

        response = await client.get(f"/api/standards/{standard_id}")

        assert response.status_code == 404

    async def test_update_standard(self, client, mock_service):
        """PATCH /api/standards/{id} — 200."""
        standard_id = uuid4()
        updated = _make_standard(
            id=standard_id,
            type=ProjectStandardType.FORMAT,
            value={"new": "value"},
        )
        mock_service.update.return_value = updated

        response = await client.patch(
            f"/api/standards/{standard_id}",
            json={"type": "format", "value": {"new": "value"}},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "format"

    async def test_delete_standard(self, client, mock_service):
        """DELETE /api/standards/{id} — 204."""
        standard_id = uuid4()

        response = await client.delete(f"/api/standards/{standard_id}")

        assert response.status_code == 204

    async def test_create_standard_invalid_type(self, client, mock_service):
        """POST с невалидным type — 422."""
        premise_id = uuid4()

        response = await client.post(
            f"/api/premises/{premise_id}/standards",
            json={"type": "invalid_type", "value": {}},
        )

        assert response.status_code == 422
