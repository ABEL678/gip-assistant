"""Тесты роутов Norm (6 тестов).

httpx.AsyncClient + ASGITransport, отдельный FastAPI app,
мок сервиса через dependency_overrides.
"""

from datetime import UTC, date, datetime
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from backend.src.domain.value_objects.enums import NormType


def _make_norm(
    id: UUID = None,
    project_id: UUID = None,
    code: str = "ГОСТ Р 21.101-2026",
):
    """Мок доменной сущности Norm (dataclass-like)."""
    norm = AsyncMock()
    norm.id = id or uuid4()
    norm.project_id = project_id or uuid4()
    norm.code = code
    norm.title = "Основные положения"
    norm.norm_type = NormType.GOST
    norm.issued_at = date(2026, 1, 1)
    norm.source_url = "https://gost.ru"
    norm.document_id = None
    norm.created_at = datetime.now(UTC)
    norm.updated_at = datetime.now(UTC)
    return norm


class TestNormsRoutes:
    """Тесты роутов Norm."""

    @pytest.fixture
    async def mock_service(self):
        """Мокированный NormService."""
        service = AsyncMock()
        service.get = AsyncMock()
        service.list_by_project = AsyncMock()
        service.create = AsyncMock()
        service.update = AsyncMock()
        service.delete = AsyncMock()
        return service

    @pytest.fixture
    async def client(self, mock_service):
        """AsyncClient с моками зависимостей."""
        from backend.src.adapters.api.dependencies import get_norm_service
        from backend.src.adapters.api.routes.norms import router as norms_router

        app = FastAPI()
        app.include_router(norms_router)

        app.dependency_overrides[get_norm_service] = lambda: mock_service

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

        app.dependency_overrides.clear()

    async def test_list_norms(self, client, mock_service):
        """GET /api/projects/{id}/norms — 200, список."""
        project_id = uuid4()
        mock_service.list_by_project.return_value = [_make_norm()]

        response = await client.get(f"/api/projects/{project_id}/norms")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["code"] == "ГОСТ Р 21.101-2026"

    async def test_create_norm(self, client, mock_service):
        """POST /api/projects/{id}/norms — 201."""
        project_id = uuid4()
        created = _make_norm(project_id=project_id)
        mock_service.create.return_value = created

        response = await client.post(
            f"/api/projects/{project_id}/norms",
            json={
                "code": "ГОСТ Р 21.101-2026",
                "title": "Основные положения",
                "norm_type": "gost",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["code"] == "ГОСТ Р 21.101-2026"
        assert data["norm_type"] == "gost"

    async def test_create_norm_duplicate_code(self, client, mock_service):
        """POST: дубль code — ValueError из сервиса — 400, не 500."""
        project_id = uuid4()
        mock_service.create.side_effect = ValueError(
            "Норма с обозначением ГОСТ Р 21.101-2026 уже существует в проекте"
        )

        response = await client.post(
            f"/api/projects/{project_id}/norms",
            json={
                "code": "ГОСТ Р 21.101-2026",
                "title": "Основные положения",
                "norm_type": "gost",
            },
        )

        assert response.status_code == 400
        assert "уже существует" in response.json()["detail"]

    async def test_get_norm_not_found(self, client, mock_service):
        """GET /api/norms/{id} — 404."""
        mock_service.get.return_value = None

        response = await client.get(f"/api/norms/{uuid4()}")

        assert response.status_code == 404

    async def test_update_norm(self, client, mock_service):
        """PATCH /api/norms/{id} — 200."""
        norm_id = uuid4()
        updated = _make_norm(id=norm_id, code="СНиП 1.0")
        mock_service.update.return_value = updated

        response = await client.patch(
            f"/api/norms/{norm_id}",
            json={"code": "СНиП 1.0"},
        )

        assert response.status_code == 200
        assert response.json()["code"] == "СНиП 1.0"

    async def test_delete_norm(self, client, mock_service):
        """DELETE /api/norms/{id} — 204."""
        response = await client.delete(f"/api/norms/{uuid4()}")

        assert response.status_code == 204
