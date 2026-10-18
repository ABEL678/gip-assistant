"""Тесты роутов Goal (10 тестов).

Используем httpx.AsyncClient + AsyncFixtures для обхода проблемы
FastAPI 0.143.x + TestClient (middleware не инициализирует AsyncExitStack).
"""

from datetime import UTC, date, datetime
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from backend.src.domain.value_objects.enums import GoalState, PremiseCategory, VerificationStatus


def _make_goal(
    id: UUID = None,
    project_id: UUID = None,
    formulation: str = "Разработать модуль",
    premise_ids: list = None,
    deadline: date = None,
    responsible_id: UUID = None,
    priority: int = 1,
    state: GoalState = GoalState.PLAN,
    verification_status: VerificationStatus = VerificationStatus.REQUIRES_CHECK,
    created_by: UUID = None,
    created_at: datetime = None,
    updated_at: datetime = None,
):
    """Создать мок goal dataclass-like object."""
    goal = AsyncMock()
    goal.id = id or uuid4()
    goal.project_id = project_id or uuid4()
    goal.formulation = formulation
    goal.premise_ids = premise_ids or []
    goal.deadline = deadline
    goal.responsible_id = responsible_id
    goal.priority = priority
    goal.state = state
    goal.verification_status = verification_status
    goal.created_by = created_by
    goal.created_at = created_at or datetime.now(UTC)
    goal.updated_at = updated_at or datetime.now(UTC)
    return goal


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
    premise.created_at = created_at or datetime.now(UTC)
    premise.updated_at = updated_at or datetime.now(UTC)
    return premise


def _make_goal_proposal(
    id: UUID = None,
    premise_id: UUID = None,
    formulation: str = "Предложенная цель",
    confidence: float = 0.8,
    created_at: datetime = None,
    rule: str = "договор_срок",
    deadline: date = None,
    priority: int = 1,
    premise_ids: list = None,
):
    """Создать мок goal proposal dataclass-like object."""
    proposal = AsyncMock()
    proposal.id = id or uuid4()
    premise = _make_premise(id=premise_id)
    premise.id = premise_id or uuid4()
    proposal.premise = premise
    proposal.formulation = formulation
    proposal.confidence = confidence
    proposal.created_at = created_at or datetime.now(UTC)
    proposal.rule = rule
    proposal.deadline = deadline
    proposal.priority = priority
    proposal.premise_ids = premise_ids or []
    proposal.verification_status = VerificationStatus.REQUIRES_CHECK
    return proposal


class TestGoalsRoutes:
    """Тесты роутов Goal."""

    @pytest.fixture
    async def mock_goal_service(self):
        """Мокированный GoalService."""
        service = AsyncMock()
        service.get = AsyncMock()
        service.list_by_project = AsyncMock()
        service.create = AsyncMock()
        service.update = AsyncMock()
        service.delete = AsyncMock()
        return service

    @pytest.fixture
    async def mock_proposal_service(self):
        """Мокированный GoalProposalService."""
        service = AsyncMock()
        service.propose_goals = AsyncMock()
        return service

    @pytest.fixture
    async def client(self, mock_goal_service, mock_proposal_service):
        """Создаём AsyncClient с моками зависимостей."""
        from backend.src.adapters.api.dependencies import (
            get_goal_proposal_service,
            get_goal_service,
        )
        from backend.src.adapters.api.routes.goals import router as goals_router

        app = FastAPI()
        app.include_router(goals_router)

        # Мокируем зависимости
        app.dependency_overrides[get_goal_service] = lambda: mock_goal_service
        app.dependency_overrides[get_goal_proposal_service] = lambda: mock_proposal_service

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

        # Очистка
        app.dependency_overrides.clear()

    async def test_get_goals_list(self, client, mock_goal_service):
        """GET /api/projects/{id}/goals — список."""
        project_id = uuid4()
        goal_obj = _make_goal(
            id=uuid4(),
            formulation="Разработать модуль",
            state=GoalState.PLAN,
        )
        mock_goal_service.list_by_project.return_value = [goal_obj]

        response = await client.get(f"/api/projects/{project_id}/goals")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["formulation"] == "Разработать модуль"

    async def test_create_goal(self, client, mock_goal_service):
        """POST /api/projects/{id}/goals — 201, создаёт."""
        project_id = uuid4()
        created_goal = _make_goal(
            id=uuid4(),
            formulation="Новая цель",
            state=GoalState.PLAN,
        )
        mock_goal_service.create.return_value = created_goal

        response = await client.post(
            f"/api/projects/{project_id}/goals",
            json={
                "formulation": "Новая цель",
                "premise_ids": [str(uuid4())],
                "deadline": None,
                "responsible_id": None,
                "priority": 1,
                "state": "plan",
                "verification_status": "requires_check",
                "created_by": None,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["formulation"] == "Новая цель"
        assert "id" in data

    async def test_get_goal_by_id(self, client, mock_goal_service):
        """GET /api/goals/{id} — 200."""
        goal_id = uuid4()
        goal_obj = _make_goal(id=goal_id, formulation="Цель по ID")
        mock_goal_service.get.return_value = goal_obj

        response = await client.get(f"/api/goals/{goal_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(goal_id)

    async def test_get_goal_proposals(self, client, mock_proposal_service):
        """GET /api/projects/{id}/goals/proposals — список предложений."""
        project_id = uuid4()
        proposal_obj = _make_goal_proposal(
            id=uuid4(),
            formulation="Предложенная цель",
            confidence=0.85,
        )
        mock_proposal_service.propose_goals.return_value = [proposal_obj]

        response = await client.get(f"/api/projects/{project_id}/goals/proposals")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["formulation"] == "Предложенная цель"

    async def test_approve_goal_proposal(self, client, mock_goal_service):
        """POST /api/projects/{id}/goals/from-proposal — 201, создаёт Goal."""
        project_id = uuid4()
        created_goal = _make_goal(
            id=uuid4(),
            formulation="Утверждённая цель",
            state=GoalState.IN_PROGRESS,
        )
        mock_goal_service.create.return_value = created_goal

        response = await client.post(
            f"/api/projects/{project_id}/goals/from-proposal",
            json={
                "formulation": "Утверждённая цель",
                "premise_ids": [str(uuid4())],
                "deadline": None,
                "priority": 1,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["formulation"] == "Утверждённая цель"

    async def test_update_goal(self, client, mock_goal_service):
        """PATCH /api/goals/{id} — 200, обновляет."""
        goal_id = uuid4()
        updated_goal = _make_goal(
            id=goal_id,
            formulation="Обновлённая цель",
            state=GoalState.IN_PROGRESS,
        )
        mock_goal_service.update.return_value = updated_goal

        response = await client.patch(
            f"/api/goals/{goal_id}",
            json={
                "formulation": "Обновлённая цель",
                "state": "in_progress",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["formulation"] == "Обновлённая цель"

    async def test_delete_goal(self, client, mock_goal_service):
        """DELETE /api/goals/{id} — 204."""
        goal_id = uuid4()

        response = await client.delete(f"/api/goals/{goal_id}")

        assert response.status_code == 204

    async def test_get_goal_not_found(self, client, mock_goal_service):
        """GET /api/goals/{nonexistent} — 404."""
        goal_id = uuid4()
        mock_goal_service.get.return_value = None

        response = await client.get(f"/api/goals/{goal_id}")

        assert response.status_code == 404

    async def test_create_goal_empty_formulation(self, client, mock_goal_service):
        """POST с пустой formulation — 422 (validation error)."""
        project_id = uuid4()

        response = await client.post(
            f"/api/projects/{project_id}/goals",
            json={
                "formulation": "",  # пустая formulation
                "premise_ids": [],
                "deadline": None,
                "responsible_id": None,
                "priority": 1,
                "state": "plan",
                "created_by": None,
            },
        )

        # Pydantic вернёт 422 для пустой formulation (min_length validation)
        assert response.status_code == 422

    async def test_create_goal_invalid_premise_id(self, client, mock_goal_service):
        """POST с невалидным premise_id — 422 (UUID validation)."""
        project_id = uuid4()

        response = await client.post(
            f"/api/projects/{project_id}/goals",
            json={
                "formulation": "Цель с неверным ID",
                "premise_ids": ["not-a-uuid"],  # невалидный UUID
                "deadline": None,
                "responsible_id": None,
                "priority": 1,
                "state": "plan",
                "created_by": None,
            },
        )

        # Pydantic вернёт 422 для невалидного UUID
        assert response.status_code == 422

    async def test_create_goal_with_deadline(self, client, mock_goal_service):
        """POST с deadline — 201, ISO формат."""
        project_id = uuid4()
        created_goal = _make_goal(
            id=uuid4(),
            formulation="Цель со сроком",
            deadline=date(2026, 12, 31),
        )
        mock_goal_service.create.return_value = created_goal

        response = await client.post(
            f"/api/projects/{project_id}/goals",
            json={
                "formulation": "Цель со сроком",
                "premise_ids": [str(uuid4())],
                "deadline": "2026-12-31",
                "responsible_id": None,
                "priority": 2,
                "state": "plan",
                "verification_status": "requires_check",
                "created_by": None,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["formulation"] == "Цель со сроком"
        assert data["deadline"] == "2026-12-31"


# ============================================================
# Интеграционные тесты с реальной БД
# ============================================================


class TestGoalPremiseIdsIntegration:
    """Интеграционные тесты: реальный FastAPI app + реальная БД."""

    @pytest.fixture
    async def db_session(self):
        """Создаём сессию с транзакцией для изоляции."""
        from backend.src.adapters.db.session import AsyncSessionLocal

        async with AsyncSessionLocal() as session:
            # Начинаем транзакцию
            async with session.begin():
                yield session
            # После теста — rollback (данные не сохраняются)

    @pytest.fixture
    async def app(self, db_session):
        """Создаём FastAPI app с реальными зависимостями."""
        from fastapi import FastAPI

        from backend.src.adapters.api.dependencies import (
            get_db_session,
            get_goal_repo,
            get_goal_service,
            get_premise_repo,
            get_premise_service,
            get_project_repo,
        )
        from backend.src.adapters.api.routes.goals import router as goals_router
        from backend.src.adapters.api.routes.premises import router as premises_router
        from backend.src.adapters.api.routes.projects import router as projects_router
        from backend.src.adapters.db.repositories.goal_repository import (
            SqlAlchemyGoalRepository,
        )
        from backend.src.adapters.db.repositories.premise_repository import (
            SqlAlchemyPremiseRepository,
        )
        from backend.src.adapters.db.repositories.project_repo import (
            SqlAlchemyProjectRepository,
        )
        from backend.src.domain.services.goal_service import GoalService
        from backend.src.domain.services.premise_service import PremiseService

        app = FastAPI()
        app.include_router(projects_router)
        app.include_router(premises_router)
        app.include_router(goals_router)

        # Переопределяем сессию на нашу тестовую
        async def _get_db():
            yield db_session

        app.dependency_overrides[get_db_session] = _get_db
        app.dependency_overrides[get_project_repo] = lambda: SqlAlchemyProjectRepository(
            db_session
        )
        app.dependency_overrides[get_premise_repo] = lambda: SqlAlchemyPremiseRepository(
            db_session
        )
        app.dependency_overrides[get_goal_repo] = lambda: SqlAlchemyGoalRepository(
            db_session
        )
        app.dependency_overrides[get_premise_service] = lambda: PremiseService(
            repo=SqlAlchemyPremiseRepository(db_session)
        )
        app.dependency_overrides[get_goal_service] = lambda: GoalService(
            repo=SqlAlchemyGoalRepository(db_session),
            premise_repo=SqlAlchemyPremiseRepository(db_session),
        )

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

    async def test_goal_premise_ids_persist_end_to_end(
        self, app: AsyncClient
    ):
        """Создать project → premise → goal.
        PATCH {premise_ids: [id]} → GET → [id].
        PATCH {premise_ids: []} → GET → [].
        PATCH {premise_ids: [другой]} → GET → [другой]."""
        # 1. Создаём проект
        resp = await app.post(
            "/api/projects",
            json={"name": "Test Project", "code": "TEST-001"},
        )
        assert resp.status_code == 201
        project_data = resp.json()
        project_id = UUID(project_data["id"])

        # 2. Создаём первую вводную
        premise1_id = uuid4()
        resp = await app.post(
            f"/api/projects/{project_id}/premises",
            json={
                "category": "contract",
                "name": "Первая вводная",
                "source": "test",
                "date": None,
                "actual": True,
                "mandatory": True,
                "link": None,
                "valid_until": None,
                "data": {},
                "schema": {},
            },
        )
        assert resp.status_code == 201
        premise1_data = resp.json()
        premise1_id = UUID(premise1_data["id"])

        # 3. Создаём вторую вводную
        resp = await app.post(
            f"/api/projects/{project_id}/premises",
            json={
                "category": "contract",
                "name": "Вторая вводная",
                "source": "test",
                "date": None,
                "actual": True,
                "mandatory": True,
                "link": None,
                "valid_until": None,
                "data": {},
                "schema": {},
            },
        )
        assert resp.status_code == 201
        premise2_data = resp.json()
        premise2_id = UUID(premise2_data["id"])

        # 4. Создаём цель без связей
        goal_id = uuid4()
        resp = await app.post(
            f"/api/projects/{project_id}/goals",
            json={
                "formulation": "Тестовая цель",
                "premise_ids": [],
                "deadline": None,
                "responsible_id": None,
                "priority": 1,
                "state": "plan",
                "verification_status": "requires_check",
                "created_by": None,
            },
        )
        assert resp.status_code == 201
        goal_data = resp.json()
        goal_id = UUID(goal_data["id"])
        assert goal_data["premise_ids"] == []

        # 5. PATCH: добавляем первую вводную
        resp = await app.patch(
            f"/api/goals/{goal_id}",
            json={"premise_ids": [str(premise1_id)]},
        )
        assert resp.status_code == 200
        goal_data = resp.json()
        assert sorted(goal_data["premise_ids"]) == [str(premise1_id)]

        # 6. GET /goals/{id} — проверяем premise_ids
        resp = await app.get(f"/api/goals/{goal_id}")
        assert resp.status_code == 200
        goal_data = resp.json()
        assert sorted(goal_data["premise_ids"]) == [str(premise1_id)]

        # 7. GET /projects/{id}/goals — проверяем premise_ids у цели
        resp = await app.get(f"/api/projects/{project_id}/goals")
        assert resp.status_code == 200
        goals_data = resp.json()
        goal_from_list = next(
            g for g in goals_data if UUID(g["id"]) == goal_id
        )
        assert sorted(goal_from_list["premise_ids"]) == [str(premise1_id)]

        # 8. PATCH: очищаем premise_ids
        resp = await app.patch(
            f"/api/goals/{goal_id}",
            json={"premise_ids": []},
        )
        assert resp.status_code == 200
        goal_data = resp.json()
        assert goal_data["premise_ids"] == []

        # 9. GET — убеждаемся, что пусто
        resp = await app.get(f"/api/goals/{goal_id}")
        assert resp.status_code == 200
        goal_data = resp.json()
        assert goal_data["premise_ids"] == []

        # 10. PATCH: заменяем на вторую вводную
        resp = await app.patch(
            f"/api/goals/{goal_id}",
            json={"premise_ids": [str(premise2_id)]},
        )
        assert resp.status_code == 200
        goal_data = resp.json()
        assert sorted(goal_data["premise_ids"]) == [str(premise2_id)]

        # 11. GET — убеждаемся, что заменилась
        resp = await app.get(f"/api/goals/{goal_id}")
        assert resp.status_code == 200
        goal_data = resp.json()
        assert sorted(goal_data["premise_ids"]) == [str(premise2_id)]
