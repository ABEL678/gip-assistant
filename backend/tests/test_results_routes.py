"""Тесты роутов Result (6 тестов).

Используем httpx.AsyncClient + ASGITransport.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient


def _make_result(
    id: UUID = None,
    project_id: UUID = None,
    formulation: str = "Результат",
    source: str = "test",
    approved_by: UUID = None,
    created_at: datetime = None,
    updated_at: datetime = None,
):
    """Создать мок result."""
    result = AsyncMock()
    result.id = id or uuid4()
    result.project_id = project_id or uuid4()
    result.formulation = formulation
    result.source = source
    result.approved_by = approved_by
    result.created_at = created_at or datetime.now(timezone.utc)
    result.updated_at = updated_at or datetime.now(timezone.utc)
    return result


class TestResultsRoutes:
    """Тесты роутов Result."""

    @pytest.fixture
    async def mock_service(self):
        """Мокированный ResultService."""
        service = AsyncMock()
        service.get_by_id = AsyncMock()
        service.list_by_project = AsyncMock()
        service.create = AsyncMock()
        service.update = AsyncMock()
        service.delete = AsyncMock()
        return service

    @pytest.fixture
    async def client(self, mock_service):
        """Создаём AsyncClient с моками зависимостей."""
        from backend.src.adapters.api.dependencies import get_result_service
        from backend.src.adapters.api.routes.results import router as results_router

        app = FastAPI()
        app.include_router(results_router)

        app.dependency_overrides[get_result_service] = lambda: mock_service

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

        app.dependency_overrides.clear()

    async def test_list_results(self, client, mock_service):
        """GET /api/projects/{id}/results — список."""
        project_id = uuid4()
        result_obj = _make_result(id=uuid4(), formulation="Результат 1")
        mock_service.list_by_project.return_value = [result_obj]

        response = await client.get(f"/api/projects/{project_id}/results")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["formulation"] == "Результат 1"

    async def test_create_result(self, client, mock_service):
        """POST /api/projects/{id}/results — 201."""
        project_id = uuid4()
        created = _make_result(id=uuid4(), formulation="Новый результат")
        mock_service.create.return_value = created

        response = await client.post(
            f"/api/projects/{project_id}/results",
            json={"formulation": "Новый результат", "source": "test"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["formulation"] == "Новый результат"
        assert "id" in data

    async def test_get_result_by_id(self, client, mock_service):
        """GET /api/results/{id} — 200."""
        result_id = uuid4()
        result_obj = _make_result(id=result_id, formulation="Результат по ID")
        mock_service.get_by_id.return_value = result_obj

        response = await client.get(f"/api/results/{result_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(result_id)

    async def test_get_result_not_found(self, client, mock_service):
        """GET /api/results/{nonexistent} — 404."""
        result_id = uuid4()
        mock_service.get_by_id.return_value = None

        response = await client.get(f"/api/results/{result_id}")

        assert response.status_code == 404

    async def test_update_result(self, client, mock_service):
        """PATCH /api/results/{id} — 200."""
        result_id = uuid4()
        updated = _make_result(
            id=result_id,
            formulation="Обновлённый результат",
            source="updated",
        )
        mock_service.update.return_value = updated

        response = await client.patch(
            f"/api/results/{result_id}",
            json={"formulation": "Обновлённый результат", "source": "updated"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["formulation"] == "Обновлённый результат"

    async def test_delete_result(self, client, mock_service):
        """DELETE /api/results/{id} — 204."""
        result_id = uuid4()

        response = await client.delete(f"/api/results/{result_id}")

        assert response.status_code == 204

    async def test_create_result_empty_formulation(self, client, mock_service):
        """POST с пустой formulation — 422."""
        project_id = uuid4()

        response = await client.post(
            f"/api/projects/{project_id}/results",
            json={"formulation": ""},
        )

        assert response.status_code == 422
