"""Тесты роутов DecisionLink (6 тестов).

httpx.AsyncClient + ASGITransport, отдельный FastAPI app,
мок сервиса через dependency_overrides.
"""

from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from backend.src.domain.value_objects.enums import DecisionLinkType


def _make_link(
    id: UUID = None,
    project_id: UUID = None,
    from_id: UUID = None,
    to_id: UUID = None,
    link_type: DecisionLinkType = DecisionLinkType.SEQUENTIAL,
):
    """Мок доменной сущности DecisionLink (dataclass-like)."""
    link = AsyncMock()
    link.id = id or uuid4()
    link.project_id = project_id or uuid4()
    link.from_decision_id = from_id or uuid4()
    link.to_decision_id = to_id or uuid4()
    link.link_type = link_type
    link.created_at = datetime.now(UTC)
    link.updated_at = datetime.now(UTC)
    return link


class TestDecisionLinksRoutes:
    """Тесты роутов DecisionLink."""

    @pytest.fixture
    async def mock_service(self):
        """Мокированный DecisionLinkService."""
        service = AsyncMock()
        service.get_by_id = AsyncMock()
        service.list_by_project = AsyncMock()
        service.list_by_decision = AsyncMock()
        service.create = AsyncMock()
        service.delete = AsyncMock()
        return service

    @pytest.fixture
    async def client(self, mock_service):
        """AsyncClient с моками зависимостей."""
        from backend.src.adapters.api.dependencies import get_decision_link_service
        from backend.src.adapters.api.routes.decision_links import (
            router as decision_links_router,
        )

        app = FastAPI()
        app.include_router(decision_links_router)

        app.dependency_overrides[get_decision_link_service] = lambda: mock_service

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

        app.dependency_overrides.clear()

    async def test_list_links_by_project(self, client, mock_service):
        """GET /api/projects/{id}/decision-links — 200, список."""
        project_id = uuid4()
        mock_service.list_by_project.return_value = [_make_link()]

        response = await client.get(f"/api/projects/{project_id}/decision-links")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["link_type"] == "sequential"

    async def test_create_link(self, client, mock_service):
        """POST /api/projects/{id}/decision-links — 201."""
        project_id = uuid4()
        from_id, to_id = uuid4(), uuid4()
        created = _make_link(
            project_id=project_id, from_id=from_id, to_id=to_id
        )
        mock_service.create.return_value = created

        response = await client.post(
            f"/api/projects/{project_id}/decision-links",
            json={
                "from_decision_id": str(from_id),
                "to_decision_id": str(to_id),
                "link_type": "sequential",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["from_decision_id"] == str(from_id)
        assert data["to_decision_id"] == str(to_id)

    async def test_create_self_link_value_error(self, client, mock_service):
        """POST self-link — ValueError из сервиса — 400, не 500."""
        project_id = uuid4()
        mock_service.create.side_effect = ValueError(
            "Решение не может быть связано само с собой"
        )

        response = await client.post(
            f"/api/projects/{project_id}/decision-links",
            json={
                "from_decision_id": str(uuid4()),
                "to_decision_id": str(uuid4()),
                "link_type": "nested",
            },
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "Решение не может быть связано само с собой"

    async def test_get_link_not_found(self, client, mock_service):
        """GET /api/decision-links/{id} — 404."""
        mock_service.get_by_id.return_value = None

        response = await client.get(f"/api/decision-links/{uuid4()}")

        assert response.status_code == 404

    async def test_delete_link(self, client, mock_service):
        """DELETE /api/decision-links/{id} — 204; несуществующий — 404."""
        mock_service.delete.return_value = True
        response = await client.delete(f"/api/decision-links/{uuid4()}")
        assert response.status_code == 204

        mock_service.delete.return_value = False
        response = await client.delete(f"/api/decision-links/{uuid4()}")
        assert response.status_code == 404

    async def test_list_links_by_decision(self, client, mock_service):
        """GET /api/decisions/{id}/links — 200, обе стороны."""
        decision_id = uuid4()
        mock_service.list_by_decision.return_value = [
            _make_link(from_id=decision_id),
            _make_link(to_id=decision_id),
        ]

        response = await client.get(f"/api/decisions/{decision_id}/links")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
