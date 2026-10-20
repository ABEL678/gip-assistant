"""Тесты роутов Action (7 тестов).

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

from backend.src.domain.value_objects.enums import ActionState


def _make_action(
    id: UUID = None,
    project_id: UUID = None,
    formulation: str = "Тестовое действие",
    task_id: UUID = None,
    measurable_result: str = None,
    deadline: date = None,
    responsible_id: UUID = None,
    state: ActionState = ActionState.PLAN,
    created_at: datetime = None,
    updated_at: datetime = None,
):
    """Создать мок action dataclass-like object."""
    action = AsyncMock()
    action.id = id or uuid4()
    action.project_id = project_id or uuid4()
    action.formulation = formulation
    action.task_id = task_id
    action.measurable_result = measurable_result
    action.deadline = deadline
    action.responsible_id = responsible_id
    action.state = state
    action.created_at = created_at or datetime.now(timezone.utc)
    action.updated_at = updated_at or datetime.now(timezone.utc)
    return action


class TestActionsRoutes:
    """Тесты роутов Action."""

    @pytest.fixture
    async def mock_service(self):
        """Мокированный ActionService."""
        service = AsyncMock()
        service.get_by_id = AsyncMock()
        service.list_by_project = AsyncMock()
        service.list_by_task = AsyncMock()
        service.create = AsyncMock()
        service.update = AsyncMock()
        service.delete = AsyncMock()
        return service

    @pytest.fixture
    async def client(self, mock_service):
        """Создаём AsyncClient с моками зависимостей."""
        from backend.src.adapters.api.routes.actions import router as actions_router
        from backend.src.adapters.api.dependencies import get_action_service

        app = FastAPI()
        app.include_router(actions_router)

        def override_get_service():
            return mock_service

        app.dependency_overrides[get_action_service] = override_get_service

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

        # Очистка
        app.dependency_overrides.clear()

    async def test_list_actions(self, client, mock_service):
        """GET /api/projects/{id}/actions — список."""
        project_id = uuid4()
        action_obj = _make_action(
            id=uuid4(),
            formulation="Действие 1",
            state=ActionState.PLAN,
        )
        mock_service.list_by_project.return_value = [action_obj]

        response = await client.get(f"/api/projects/{project_id}/actions")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["formulation"] == "Действие 1"

    async def test_create_action(self, client, mock_service):
        """POST /api/projects/{id}/actions — 201, создаёт."""
        project_id = uuid4()
        created_action = _make_action(
            id=uuid4(),
            formulation="Новое действие",
            state=ActionState.IN_PROGRESS,
        )
        mock_service.create.return_value = created_action

        response = await client.post(
            f"/api/projects/{project_id}/actions",
            json={
                "formulation": "Новое действие",
                "state": "in_progress",
                "task_id": None,
                "measurable_result": None,
                "deadline": None,
                "responsible_id": None,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["formulation"] == "Новое действие"
        assert data["state"] == "in_progress"
        assert "id" in data

    async def test_get_action(self, client, mock_service):
        """GET /api/actions/{id} — 200."""
        action_id = uuid4()
        action_obj = _make_action(id=action_id, formulation="Договор")
        mock_service.get_by_id.return_value = action_obj

        response = await client.get(f"/api/actions/{action_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(action_id)

    async def test_get_action_not_found(self, client, mock_service):
        """GET /api/actions/{nonexistent} — 404."""
        action_id = uuid4()
        mock_service.get_by_id.return_value = None

        response = await client.get(f"/api/actions/{action_id}")

        assert response.status_code == 404

    async def test_update_action(self, client, mock_service):
        """PATCH /api/actions/{id} — 200, обновляет."""
        action_id = uuid4()
        updated_action = _make_action(
            id=action_id,
            formulation="Обновлённое действие",
            state=ActionState.DONE,
        )
        mock_service.update.return_value = updated_action

        response = await client.patch(
            f"/api/actions/{action_id}",
            json={
                "formulation": "Обновлённое действие",
                "state": "done",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["formulation"] == "Обновлённое действие"
        assert data["state"] == "done"

    async def test_delete_action(self, client, mock_service):
        """DELETE /api/actions/{id} — 204."""
        action_id = uuid4()

        response = await client.delete(f"/api/actions/{action_id}")

        assert response.status_code == 204

    async def test_list_by_task(self, client, mock_service):
        """GET /api/tasks/{id}/actions — список действий задачи."""
        task_id = uuid4()
        action_obj = _make_action(
            id=uuid4(),
            formulation="Действие задачи",
            task_id=task_id,
        )
        mock_service.list_by_task.return_value = [action_obj]

        response = await client.get(f"/api/tasks/{task_id}/actions")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["formulation"] == "Действие задачи"
