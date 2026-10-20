"""Тесты роутов Premise (7 тестов).

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

from backend.src.domain.value_objects.enums import PremiseCategory


def _make_premise(
    id: UUID = None,
    project_id: UUID = None,
    category: PremiseCategory = PremiseCategory.CONTRACT,
    name: str = "Договор",
    source: str = "test",
    date_val: date = None,
    actual: bool = True,
    mandatory: bool = True,
    link: str = None,
    valid_until: date = None,
    data: dict = None,
    schema: dict = None,
    created_at: datetime = None,
    updated_at: datetime = None,
):
    """Создать мок premise dataclass-like object."""
    premise = AsyncMock()
    premise.id = id or uuid4()
    premise.project_id = project_id or uuid4()
    premise.category = category
    premise.name = name
    premise.source = source
    premise.date = date_val
    premise.actual = actual
    premise.mandatory = mandatory
    premise.link = link
    premise.valid_until = valid_until
    premise.data = data or {}
    premise.schema = schema or {}
    premise.source_goal_id = None
    premise.created_at = created_at or datetime.now(timezone.utc)
    premise.updated_at = updated_at or datetime.now(timezone.utc)
    return premise


class TestPremisesRoutes:
    """Тесты роутов Premise."""

    @pytest.fixture
    async def mock_service(self):
        """Мокированный PremiseService."""
        service = AsyncMock()
        service.get = AsyncMock()
        service.list_by_project = AsyncMock()
        service.create = AsyncMock()
        service.update = AsyncMock()
        service.delete = AsyncMock()
        return service

    @pytest.fixture
    async def client(self, mock_service):
        """Создаём AsyncClient с моками зависимостей."""
        # Создаём тестовый FastAPI app
        from backend.src.adapters.api.routes.premises import router as premises_router
        from backend.src.adapters.api.dependencies import get_premise_service

        app = FastAPI()
        app.include_router(premises_router)

        # Мокируем зависимость
        def override_get_service():
            return mock_service

        app.dependency_overrides[get_premise_service] = override_get_service

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac
        
        # Очистка
        app.dependency_overrides.clear()

    async def test_get_premises_list(self, client, mock_service):
        """GET /api/projects/{id}/premises — список."""
        project_id = uuid4()
        premise_obj = _make_premise(
            id=uuid4(),
            name="Договор",
            category=PremiseCategory.CONTRACT,
        )
        mock_service.list_by_project.return_value = [premise_obj]

        response = await client.get(f"/api/projects/{project_id}/premises")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["name"] == "Договор"

    async def test_create_premise(self, client, mock_service):
        """POST /api/projects/{id}/premises — 201, создаёт."""
        project_id = uuid4()
        created_premise = _make_premise(
            id=uuid4(),
            name="Новая вводная",
            category=PremiseCategory.CONTRACT,
        )
        mock_service.create.return_value = created_premise

        response = await client.post(
            f"/api/projects/{project_id}/premises",
            json={
                "category": "contract",
                "name": "Новая вводная",
                "source": "test",
                "date": None,
                "actual": True,
                "mandatory": True,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Новая вводная"
        assert "id" in data

    async def test_get_premise_by_id(self, client, mock_service):
        """GET /api/premises/{id} — 200."""
        premise_id = uuid4()
        premise_obj = _make_premise(id=premise_id, name="Договор")
        mock_service.get.return_value = premise_obj

        response = await client.get(f"/api/premises/{premise_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(premise_id)

    async def test_get_premise_not_found(self, client, mock_service):
        """GET /api/premises/{nonexistent} — 404."""
        premise_id = uuid4()
        mock_service.get.return_value = None

        response = await client.get(f"/api/premises/{premise_id}")

        assert response.status_code == 404

    async def test_update_premise(self, client, mock_service):
        """PATCH /api/premises/{id} — 200, обновляет."""
        premise_id = uuid4()
        updated_premise = _make_premise(
            id=premise_id,
            name="Обновлённая вводная",
            category=PremiseCategory.TZ,
        )
        mock_service.update.return_value = updated_premise

        response = await client.patch(
            f"/api/premises/{premise_id}",
            json={"name": "Обновлённая вводная", "category": "tz"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Обновлённая вводная"

    async def test_delete_premise(self, client, mock_service):
        """DELETE /api/premises/{id} — 204."""
        premise_id = uuid4()

        response = await client.delete(f"/api/premises/{premise_id}")

        assert response.status_code == 204

    async def test_create_premise_invalid_data(self, client, mock_service):
        """POST с невалидными данными — 422 (Pydantic validation)."""
        project_id = uuid4()
        # category должен быть валидным enum значением
        response = await client.post(
            f"/api/projects/{project_id}/premises",
            json={
                "category": "invalid_category",  # невалидный enum
                "name": "Test",
                "source": "test",
                "date": None,
                "actual": True,
                "mandatory": True,
            },
        )

        # Pydantic вернёт 422 для невалидного enum
        assert response.status_code == 422

    async def test_create_premise_with_date(self, client, mock_service):
        """POST с датой — 201, ISO формат."""
        project_id = uuid4()
        created_premise = _make_premise(
            id=uuid4(),
            name="Вводная с датой",
            category=PremiseCategory.CONTRACT,
            date_val=date(2026, 10, 17),
        )
        mock_service.create.return_value = created_premise

        response = await client.post(
            f"/api/projects/{project_id}/premises",
            json={
                "category": "contract",
                "name": "Вводная с датой",
                "date": "2026-10-17",
                "valid_until": "2027-01-01",
                "actual": True,
                "mandatory": True,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Вводная с датой"
        assert data["date"] == "2026-10-17"
