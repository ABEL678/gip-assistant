"""Тесты роутов Decision (9 тестов).

httpx.AsyncClient + ASGITransport (не TestClient — несовместим с
FastAPI 0.143.x + middleware). Отдельный FastAPI app на тест,
мок сервиса через app.dependency_overrides.
"""

from datetime import UTC, date, datetime
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from backend.src.domain.value_objects.enums import DecisionState


def _make_decision(
    id: UUID = None,
    project_id: UUID = None,
    formulation: str = "Определить способ реализации",
    state: DecisionState = DecisionState.PLAN,
):
    """Мок доменной сущности Decision (dataclass-like)."""
    decision = AsyncMock()
    decision.id = id or uuid4()
    decision.project_id = project_id or uuid4()
    decision.formulation = formulation
    decision.rationale = "Срок из вводных"
    decision.context = None
    decision.deadline = date(2026, 12, 1)
    decision.state = state
    decision.created_by = None
    decision.premise_ids = [uuid4(), uuid4()]
    decision.goal_ids = [uuid4()]
    decision.created_at = datetime.now(UTC)
    decision.updated_at = datetime.now(UTC)
    return decision


def _make_proposal(formulation: str = "Определить способ реализации цели: X"):
    """Мок доменной сущности DecisionProposal (эфемерная)."""
    proposal = AsyncMock()
    proposal.id = uuid4()
    proposal.formulation = formulation
    proposal.rationale = None
    proposal.state = DecisionState.PLAN
    proposal.premise_ids = []
    proposal.goal_ids = [uuid4()]
    proposal.rule = "goal_без_решения"
    return proposal


class TestDecisionsRoutes:
    """Тесты роутов Decision."""

    @pytest.fixture
    async def mock_service(self):
        """Мокированный DecisionService."""
        service = AsyncMock()
        service.get = AsyncMock()
        service.list_by_project = AsyncMock()
        service.create = AsyncMock()
        service.update = AsyncMock()
        service.delete = AsyncMock()
        return service

    @pytest.fixture
    async def mock_proposal_service(self):
        """Мокированный DecisionProposalService."""
        service = AsyncMock()
        service.propose_decisions = AsyncMock()
        return service

    @pytest.fixture
    async def client(self, mock_service, mock_proposal_service):
        """AsyncClient с моками зависимостей."""
        from backend.src.adapters.api.dependencies import (
            get_decision_proposal_service,
            get_decision_service,
        )
        from backend.src.adapters.api.routes.decisions import router as decisions_router

        app = FastAPI()
        app.include_router(decisions_router)

        app.dependency_overrides[get_decision_service] = lambda: mock_service
        app.dependency_overrides[get_decision_proposal_service] = (
            lambda: mock_proposal_service
        )

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

        app.dependency_overrides.clear()

    async def test_list_decisions(self, client, mock_service):
        """GET /api/projects/{id}/decisions — 200, список."""
        project_id = uuid4()
        mock_service.list_by_project.return_value = [_make_decision()]

        response = await client.get(f"/api/projects/{project_id}/decisions")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["formulation"] == "Определить способ реализации"

    async def test_create_decision(self, client, mock_service):
        """POST /api/projects/{id}/decisions — 201."""
        project_id = uuid4()
        created = _make_decision(project_id=project_id)
        mock_service.create.return_value = created

        response = await client.post(
            f"/api/projects/{project_id}/decisions",
            json={"formulation": "Определить способ реализации"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["formulation"] == "Определить способ реализации"
        assert data["state"] == "plan"
        assert "id" in data

    async def test_create_decision_value_error(self, client, mock_service):
        """POST: сервис кидает ValueError — 400, не 500."""
        project_id = uuid4()
        mock_service.create.side_effect = ValueError("Проект не найден")

        response = await client.post(
            f"/api/projects/{project_id}/decisions",
            json={"formulation": "Test"},
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "Проект не найден"

    async def test_get_decision_by_id(self, client, mock_service):
        """GET /api/decisions/{id} — 200."""
        decision_id = uuid4()
        mock_service.get.return_value = _make_decision(id=decision_id)

        response = await client.get(f"/api/decisions/{decision_id}")

        assert response.status_code == 200
        assert response.json()["id"] == str(decision_id)

    async def test_get_decision_not_found(self, client, mock_service):
        """GET /api/decisions/{id} — 404."""
        mock_service.get.return_value = None

        response = await client.get(f"/api/decisions/{uuid4()}")

        assert response.status_code == 404

    async def test_update_decision(self, client, mock_service):
        """PATCH /api/decisions/{id} — 200."""
        decision_id = uuid4()
        updated = _make_decision(id=decision_id, formulation="Обновлённое решение")
        mock_service.update.return_value = updated

        response = await client.patch(
            f"/api/decisions/{decision_id}",
            json={"formulation": "Обновлённое решение"},
        )

        assert response.status_code == 200
        assert response.json()["formulation"] == "Обновлённое решение"

    async def test_delete_decision(self, client, mock_service):
        """DELETE /api/decisions/{id} — 204."""
        response = await client.delete(f"/api/decisions/{uuid4()}")

        assert response.status_code == 204

    async def test_get_decision_proposals(self, client, mock_proposal_service):
        """GET /api/projects/{id}/decisions/proposals — 200."""
        project_id = uuid4()
        mock_proposal_service.propose_decisions.return_value = [_make_proposal()]

        response = await client.get(
            f"/api/projects/{project_id}/decisions/proposals"
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["rule"] == "goal_без_решения"

    async def test_approve_decision_proposal(self, client, mock_service):
        """POST /api/projects/{id}/decisions/from-proposal — 201."""
        project_id = uuid4()
        created = _make_decision(
            project_id=project_id,
            formulation="Определить способ реализации цели: X",
        )
        mock_service.create.return_value = created

        response = await client.post(
            f"/api/projects/{project_id}/decisions/from-proposal",
            json={
                "formulation": "Определить способ реализации цели: X",
                "rationale": "Срок из вводных",
                "premise_ids": [str(uuid4())],
                "goal_ids": [str(uuid4())],
            },
        )

        assert response.status_code == 201
        assert response.json()["formulation"] == "Определить способ реализации цели: X"
