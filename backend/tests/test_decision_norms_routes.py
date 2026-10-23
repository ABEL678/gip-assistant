"""Тесты роутов DecisionNorm (5 тестов).

httpx.AsyncClient + ASGITransport, отдельный FastAPI app,
мок сервиса через dependency_overrides.
"""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient


class TestDecisionNormsRoutes:
    """Тесты роутов DecisionNorm (связь Decision ↔ Norm)."""

    @pytest.fixture
    async def mock_service(self):
        """Мокированный DecisionNormService."""
        service = AsyncMock()
        service.link = AsyncMock()
        service.unlink = AsyncMock()
        service.list_norms_by_decision = AsyncMock()
        service.list_decisions_by_norm = AsyncMock()
        return service

    @pytest.fixture
    async def client(self, mock_service):
        """AsyncClient с моками зависимостей."""
        from backend.src.adapters.api.dependencies import get_decision_norm_service
        from backend.src.adapters.api.routes.decision_norms import (
            router as decision_norms_router,
        )

        app = FastAPI()
        app.include_router(decision_norms_router)

        app.dependency_overrides[get_decision_norm_service] = lambda: mock_service

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

        app.dependency_overrides.clear()

    async def test_link_decision_norm(self, client, mock_service):
        """POST /api/decisions/{id}/norms/{norm_id} — 204."""
        response = await client.post(
            f"/api/decisions/{uuid4()}/norms/{uuid4()}"
        )

        assert response.status_code == 204
        mock_service.link.assert_called_once()

    async def test_link_value_error(self, client, mock_service):
        """POST: разные проекты — ValueError — 400, не 500."""
        mock_service.link.side_effect = ValueError(
            "Нельзя связать решение и норму из разных проектов"
        )

        response = await client.post(
            f"/api/decisions/{uuid4()}/norms/{uuid4()}"
        )

        assert response.status_code == 400
        assert "разных проектов" in response.json()["detail"]

    async def test_unlink_decision_norm(self, client, mock_service):
        """DELETE /api/decisions/{id}/norms/{norm_id} — 204."""
        response = await client.delete(
            f"/api/decisions/{uuid4()}/norms/{uuid4()}"
        )

        assert response.status_code == 204
        mock_service.unlink.assert_called_once()

    async def test_list_norms_by_decision(self, client, mock_service):
        """GET /api/decisions/{id}/norms — 200, массив UUID-строк."""
        norm_ids = [uuid4(), uuid4()]
        mock_service.list_norms_by_decision.return_value = norm_ids

        response = await client.get(f"/api/decisions/{uuid4()}/norms")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0] == str(norm_ids[0])

    async def test_list_decisions_by_norm(self, client, mock_service):
        """GET /api/norms/{id}/decisions — 200, массив UUID-строк."""
        decision_ids = [uuid4()]
        mock_service.list_decisions_by_norm.return_value = decision_ids

        response = await client.get(f"/api/norms/{uuid4()}/decisions")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert data[0] == str(decision_ids[0])
