"""Тесты роутов RFI (14 тестов).

Используем httpx.AsyncClient + AsyncFixtures для обхода проблемы
FastAPI 0.143.x + TestClient (middleware не инициализирует AsyncExitStack).
"""

from datetime import date, datetime, timezone
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
import httpx
from httpx import ASGITransport, AsyncClient
from fastapi import FastAPI

from backend.src.domain.entities.task import Task
from backend.src.domain.value_objects.enums import RfiState, TaskStatus
from backend.src.application.dto.rfi import RfiProposal


def _make_task(
    id: UUID = None,
    project_id: UUID = None,
    title: str = "RFI Test",
    status: TaskStatus = TaskStatus.NOT_STARTED,
    is_rfi: bool = True,
    rfi_state: RfiState = None,
    rfi_cause_decision_id: UUID = None,
    rfi_cause_goal_id: UUID = None,
    rfi_due_date: date = None,
    deadline: date = None,
    assignee_id: UUID = None,
    is_complex: bool = False,
    description: str = None,
    premise_ids: list = None,
    sort_order: int = 0,
    source: str = "manual",
    created_at: datetime = None,
    updated_at: datetime = None,
):
    """Создать мок Task dataclass-like object."""
    return Task(
        id=id or uuid4(),
        project_id=project_id or uuid4(),
        title=title,
        description=description,
        status=status,
        is_rfi=is_rfi,
        rfi_state=rfi_state,
        rfi_cause_decision_id=rfi_cause_decision_id,
        rfi_cause_goal_id=rfi_cause_goal_id,
        rfi_due_date=rfi_due_date,
        deadline=deadline,
        assignee_id=assignee_id,
        is_complex=is_complex,
        premise_ids=premise_ids or [],
        sort_order=sort_order,
        source=source,
        created_at=created_at or datetime.now(timezone.utc),
        updated_at=updated_at or datetime.now(timezone.utc),
    )


def _make_proposal(
    id: UUID = None,
    action: str = "create",
    rule: str = "decision_без_ид",
    formulation: str = "Test formulation",
    rationale: str = None,
    reason_decision_id: UUID = None,
    existing_rfi_id: UUID = None,
    rfi_due_date: date = None,
):
    """Создать мок RfiProposal."""
    return RfiProposal(
        id=id or uuid4(),
        action=action,
        rule=rule,
        formulation=formulation,
        rationale=rationale,
        reason_decision_id=reason_decision_id,
        existing_rfi_id=existing_rfi_id,
        rfi_due_date=rfi_due_date,
    )


class TestRfisRoutes:
    """Тесты роутов RFI."""

    @pytest.fixture
    async def mock_rfi_service(self):
        """Мокированный RfiService."""
        service = AsyncMock()
        service.create = AsyncMock()
        service.list_by_project = AsyncMock()
        service.get = AsyncMock()
        service.update = AsyncMock()
        service.delete = AsyncMock()
        service.escalate = AsyncMock()
        return service

    @pytest.fixture
    async def mock_proposal_service(self):
        """Мокированный RfiProposalService."""
        service = AsyncMock()
        service.propose_rfis = AsyncMock()
        return service

    @pytest.fixture
    async def client(self, mock_rfi_service, mock_proposal_service):
        """Создаём AsyncClient с моками зависимостей."""
        from backend.src.adapters.api.routes.rfis import router as rfis_router
        from backend.src.adapters.api.dependencies import (
            get_rfi_service,
            get_rfi_proposal_service,
        )

        app = FastAPI()
        app.include_router(rfis_router)

        def override_get_rfi_service():
            return mock_rfi_service

        def override_get_proposal_service():
            return mock_proposal_service

        app.dependency_overrides[get_rfi_service] = override_get_rfi_service
        app.dependency_overrides[get_rfi_proposal_service] = override_get_proposal_service

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

        app.dependency_overrides.clear()

    # --- #1 GET /proposals ---

    async def test_get_proposals(self, client, mock_proposal_service):
        """GET /projects/{id}/rfis/proposals — 200, список RfiProposal с id."""
        project_id = uuid4()
        proposal = _make_proposal(
            id=uuid4(),
            action="create",
            rule="decision_без_ид",
            formulation="Запросить ИД для решения",
        )
        mock_proposal_service.propose_rfis.return_value = [proposal]

        response = await client.get(f"/api/projects/{project_id}/rfis/proposals")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["action"] == "create"
        assert data[0]["id"] is not None  # uuid5 из сервиса

    # --- #2 POST /from-proposal ---

    async def test_from_proposal_create(self, client, mock_rfi_service):
        """POST /from-proposal — 201, маппинг formulation→title, rationale→description."""
        project_id = uuid4()
        created = _make_task(
            id=uuid4(),
            project_id=project_id,
            title="Запросить ИД для решения X",
        )
        mock_rfi_service.create.return_value = created

        response = await client.post(
            f"/api/projects/{project_id}/rfis/from-proposal",
            json={
                "formulation": "Запросить ИД для решения X",
                "rationale": "Не хватает исходных данных",
                "rfi_cause_decision_id": str(uuid4()),
                "rfi_due_date": "2026-11-07",
                "rfi_state": "open",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Запросить ИД для решения X"
        # Проверка маппинга в мок-вызов
        mock_rfi_service.create.assert_called_once()
        call_kwargs = mock_rfi_service.create.call_args
        assert call_kwargs.kwargs["title"] == "Запросить ИД для решения X"
        assert call_kwargs.kwargs["description"] == "Не хватает исходных данных"

    # --- #3 GET /projects/{id}/rfis ---

    async def test_list_rfis(self, client, mock_rfi_service):
        """GET /projects/{id}/rfis — 200, список RfiRead."""
        project_id = uuid4()
        task = _make_task(
            id=uuid4(),
            project_id=project_id,
            rfi_state=RfiState.OPEN,
            title="RFI Test",
        )
        mock_rfi_service.list_by_project.return_value = [task]

        response = await client.get(f"/api/projects/{project_id}/rfis")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["title"] == "RFI Test"

    # --- #4 POST /projects/{id}/rfis ---

    async def test_create_rfi(self, client, mock_rfi_service):
        """POST /projects/{id}/rfis — 201, создаёт RFI."""
        project_id = uuid4()
        created = _make_task(
            id=uuid4(),
            project_id=project_id,
            rfi_state=RfiState.OPEN,
            title="Новый RFI",
        )
        mock_rfi_service.create.return_value = created

        response = await client.post(
            f"/api/projects/{project_id}/rfis",
            json={
                "title": "Новый RFI",
                "rfi_cause_decision_id": str(uuid4()),
                "rfi_due_date": "2026-11-07",
                "rfi_state": "open",
                "deadline": None,
                "assignee_id": None,
                "is_complex": False,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Новый RFI"

    # --- #5 POST /projects/{id}/rfis — 400 XOR ---

    async def test_create_rfi_xor_both_null(self, client, mock_rfi_service):
        """POST /projects/{id}/rfis — 400, обе причины NULL."""
        project_id = uuid4()
        mock_rfi_service.create.side_effect = ValueError(
            "Ровно одна причина обязательна: rfi_cause_decision_id XOR rfi_cause_goal_id"
        )

        response = await client.post(
            f"/api/projects/{project_id}/rfis",
            json={
                "title": "Новый RFI",
                "rfi_cause_decision_id": None,
                "rfi_cause_goal_id": None,
                "rfi_due_date": None,
                "rfi_state": "open",
                "deadline": None,
                "assignee_id": None,
                "is_complex": False,
            },
        )

        assert response.status_code == 400

    # --- #6 GET /rfis/{id} ---

    async def test_get_rfi(self, client, mock_rfi_service):
        """GET /rfis/{id} — 200, RFI по ID."""
        task_id = uuid4()
        task = _make_task(id=task_id, rfi_state=RfiState.OPEN)
        mock_rfi_service.get.return_value = task

        response = await client.get(f"/api/rfis/{task_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(task_id)

    # --- #7 GET /rfis/{id} — 404 ---

    async def test_get_rfi_not_found(self, client, mock_rfi_service):
        """GET /rfis/{id} — 404, не найден."""
        task_id = uuid4()
        mock_rfi_service.get.return_value = None

        response = await client.get(f"/api/rfis/{task_id}")

        assert response.status_code == 404

    # --- #8 PATCH /rfis/{id} ---

    async def test_update_rfi(self, client, mock_rfi_service):
        """PATCH /rfis/{id} — 200, обновляет RFI."""
        task_id = uuid4()
        updated = _make_task(id=task_id, title="Обновлённый RFI", rfi_state=RfiState.SENT)
        mock_rfi_service.update.return_value = updated

        response = await client.patch(
            f"/api/rfis/{task_id}",
            json={"title": "Обновлённый RFI", "rfi_state": "sent"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Обновлённый RFI"

    # --- #9 PATCH /rfis/{id} — 400 XOR ---

    async def test_update_rfi_xor_both_set(self, client, mock_rfi_service):
        """PATCH /rfis/{id} — 400, XOR ревалидация (обе причины)."""
        task_id = uuid4()
        mock_rfi_service.update.side_effect = ValueError(
            "Ровно одна причина обязательна: rfi_cause_decision_id XOR rfi_cause_goal_id"
        )

        response = await client.patch(
            f"/api/rfis/{task_id}",
            json={
                "rfi_cause_decision_id": str(uuid4()),
                "rfi_cause_goal_id": str(uuid4()),
            },
        )

        assert response.status_code == 400

    # --- #10 DELETE /rfis/{id} ---

    async def test_delete_rfi(self, client, mock_rfi_service):
        """DELETE /rfis/{id} — 204."""
        task_id = uuid4()

        response = await client.delete(f"/api/rfis/{task_id}")

        assert response.status_code == 204

    # --- #11 POST /rfis/{id}/escalate ---

    async def test_escalate_rfi(self, client, mock_rfi_service):
        """POST /rfis/{id}/escalate — 200, rfi_state == 'escalated'."""
        task_id = uuid4()
        escalated = _make_task(
            id=task_id,
            rfi_state=RfiState.ESCALATED,
        )
        mock_rfi_service.escalate.return_value = escalated

        response = await client.post(f"/api/rfis/{task_id}/escalate")

        assert response.status_code == 200
        data = response.json()
        assert data["rfi_state"] == "escalated"

    # --- #12 POST /rfis/{id}/escalate — 400 ---

    async def test_escalate_rfi_not_found(self, client, mock_rfi_service):
        """POST /rfis/{id}/escalate — 400, RFI не найден."""
        task_id = uuid4()
        mock_rfi_service.escalate.side_effect = ValueError(f"RFI {task_id} не найден")

        response = await client.post(f"/api/rfis/{task_id}/escalate")

        assert response.status_code == 400

    # --- #13 POST /projects/{id}/rfis — 422 ---

    async def test_create_rfi_invalid_dto(self, client, mock_rfi_service):
        """POST /projects/{id}/rfis — 422, невалидный DTO."""
        project_id = uuid4()

        response = await client.post(
            f"/api/projects/{project_id}/rfis",
            json={
                "title": "",  # min_length=1
                "rfi_cause_decision_id": str(uuid4()),
                "rfi_due_date": None,
                "rfi_state": "open",
                "deadline": None,
                "assignee_id": None,
                "is_complex": False,
            },
        )

        assert response.status_code == 422

    # --- #14 PATCH /rfis/{id} — 404 ---

    async def test_update_rfi_not_found(self, client, mock_rfi_service):
        """PATCH /rfis/{id} — 404, не найден."""
        task_id = uuid4()
        mock_rfi_service.update.return_value = None

        response = await client.patch(
            f"/api/rfis/{task_id}",
            json={"title": "Новый заголовок"},
        )

        assert response.status_code == 404
