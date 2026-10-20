"""Тесты роутов Revision (9 тестов).

Используем httpx.AsyncClient + ASGITransport.
"""

from datetime import date, datetime, timezone
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from backend.src.domain.value_objects.enums import (
    ChangeStatus,
    RevisionDecisionType,
)


def _make_revision(
    id: UUID = None,
    document_id: UUID = None,
    version: int = 1,
    source: str = "test",
    notified: bool = False,
    stop_flag: bool = False,
    created_at: datetime = None,
    updated_at: datetime = None,
):
    """Создать мок revision."""
    revision = AsyncMock()
    revision.id = id or uuid4()
    revision.document_id = document_id or uuid4()
    revision.version = version
    revision.date = None
    revision.source = source
    revision.notified = notified
    revision.stop_flag = stop_flag
    revision.created_at = created_at or datetime.now(timezone.utc)
    revision.updated_at = updated_at or datetime.now(timezone.utc)
    return revision


def _make_change(
    id: UUID = None,
    revision_id: UUID = None,
    field: str = "title",
    status: ChangeStatus = ChangeStatus.ADDED,
    old_value: str = None,
    new_value: str = "new title",
    created_at: datetime = None,
    updated_at: datetime = None,
):
    """Создать мок change."""
    change = AsyncMock()
    change.id = id or uuid4()
    change.revision_id = revision_id or uuid4()
    change.field = field
    change.status = status
    change.old_value = old_value
    change.new_value = new_value
    change.created_at = created_at or datetime.now(timezone.utc)
    change.updated_at = updated_at or datetime.now(timezone.utc)
    return change


def _make_decision(
    id: UUID = None,
    change_id: UUID = None,
    decision: RevisionDecisionType = RevisionDecisionType.ACCEPTED,
    decided_by: UUID = None,
    deadline: date = None,
    created_at: datetime = None,
    updated_at: datetime = None,
):
    """Создать мок revision decision."""
    decision_obj = AsyncMock()
    decision_obj.id = id or uuid4()
    decision_obj.change_id = change_id or uuid4()
    decision_obj.decision = decision
    decision_obj.decided_by = decided_by
    decision_obj.deadline = deadline
    decision_obj.created_at = created_at or datetime.now(timezone.utc)
    decision_obj.updated_at = updated_at or datetime.now(timezone.utc)
    return decision_obj


def _make_stop_flag(
    id: UUID = None,
    revision_id: UUID = None,
    reason: str = "Blocking issue",
    resolved: bool = False,
    created_at: datetime = None,
    updated_at: datetime = None,
):
    """Создать мок stop flag."""
    stop_flag = AsyncMock()
    stop_flag.id = id or uuid4()
    stop_flag.revision_id = revision_id or uuid4()
    stop_flag.reason = reason
    stop_flag.resolved = resolved
    stop_flag.created_at = created_at or datetime.now(timezone.utc)
    stop_flag.updated_at = updated_at or datetime.now(timezone.utc)
    return stop_flag


class TestRevisionsRoutes:
    """Тесты роутов Revision."""

    @pytest.fixture
    async def mock_revision_service(self):
        service = AsyncMock()
        service.get_by_id = AsyncMock()
        service.list_by_document = AsyncMock()
        service.create = AsyncMock()
        service.delete = AsyncMock()
        return service

    @pytest.fixture
    async def mock_change_service(self):
        service = AsyncMock()
        service.get_by_id = AsyncMock()
        service.list_by_revision = AsyncMock()
        service.create = AsyncMock()
        service.delete = AsyncMock()
        return service

    @pytest.fixture
    async def mock_decision_service(self):
        service = AsyncMock()
        service.get_by_id = AsyncMock()
        service.list_by_change = AsyncMock()
        service.create = AsyncMock()
        service.delete = AsyncMock()
        return service

    @pytest.fixture
    async def mock_stop_flag_service(self):
        service = AsyncMock()
        service.get_by_id = AsyncMock()
        service.list_by_revision = AsyncMock()
        service.create = AsyncMock()
        service.delete = AsyncMock()
        return service

    @pytest.fixture
    async def client(
        self,
        mock_revision_service,
        mock_change_service,
        mock_decision_service,
        mock_stop_flag_service,
    ):
        from backend.src.adapters.api.dependencies import (
            get_change_service,
            get_revision_decision_service,
            get_revision_service,
            get_stop_flag_service,
        )
        from backend.src.adapters.api.routes.revisions import router as revisions_router

        app = FastAPI()
        app.include_router(revisions_router)

        app.dependency_overrides[get_revision_service] = lambda: mock_revision_service
        app.dependency_overrides[get_change_service] = lambda: mock_change_service
        app.dependency_overrides[get_revision_decision_service] = (
            lambda: mock_decision_service
        )
        app.dependency_overrides[get_stop_flag_service] = lambda: mock_stop_flag_service

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

        app.dependency_overrides.clear()

    async def test_create_revision(self, client, mock_revision_service):
        """POST /api/documents/{id}/revisions — 201."""
        document_id = uuid4()
        created = _make_revision(
            id=uuid4(),
            document_id=document_id,
            version=2,
        )
        mock_revision_service.create.return_value = created

        response = await client.post(
            f"/api/documents/{document_id}/revisions",
            json={
                "document_id": str(document_id),
                "version": 2,
                "date": None,
                "source": "test",
                "notified": False,
                "stop_flag": False,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["version"] == 2
        assert "id" in data

    async def test_list_revisions(self, client, mock_revision_service):
        """GET /api/documents/{id}/revisions — список."""
        document_id = uuid4()
        rev1 = _make_revision(id=uuid4(), version=2)
        rev2 = _make_revision(id=uuid4(), version=1)
        mock_revision_service.list_by_document.return_value = [rev1, rev2]

        response = await client.get(f"/api/documents/{document_id}/revisions")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["version"] == 2

    async def test_get_revision_by_id(self, client, mock_revision_service):
        """GET /api/revisions/{id} — 200."""
        revision_id = uuid4()
        rev = _make_revision(id=revision_id, version=1)
        mock_revision_service.get_by_id.return_value = rev

        response = await client.get(f"/api/revisions/{revision_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(revision_id)

    async def test_get_revision_not_found(self, client, mock_revision_service):
        """GET /api/revisions/{nonexistent} — 404."""
        revision_id = uuid4()
        mock_revision_service.get_by_id.return_value = None

        response = await client.get(f"/api/revisions/{revision_id}")

        assert response.status_code == 404

    async def test_create_change(self, client, mock_change_service):
        """POST /api/revisions/{id}/changes — 201."""
        revision_id = uuid4()
        created = _make_change(
            id=uuid4(),
            revision_id=revision_id,
            field="title",
            status=ChangeStatus.ADDED,
            new_value="new title",
        )
        mock_change_service.create.return_value = created

        response = await client.post(
            f"/api/revisions/{revision_id}/changes",
            json={
                "revision_id": str(revision_id),
                "field": "title",
                "status": "added",
                "old_value": None,
                "new_value": "new title",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["field"] == "title"
        assert data["status"] == "added"

    async def test_list_changes(self, client, mock_change_service):
        """GET /api/revisions/{id}/changes — список."""
        revision_id = uuid4()
        change_obj = _make_change(id=uuid4(), field="description")
        mock_change_service.list_by_revision.return_value = [change_obj]

        response = await client.get(f"/api/revisions/{revision_id}/changes")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["field"] == "description"

    async def test_create_decision(self, client, mock_decision_service):
        """POST /api/changes/{id}/decision — 201."""
        change_id = uuid4()
        created = _make_decision(
            id=uuid4(),
            change_id=change_id,
            decision=RevisionDecisionType.ACCEPTED,
        )
        mock_decision_service.create.return_value = created

        response = await client.post(
            f"/api/changes/{change_id}/decision",
            json={
                "change_id": str(change_id),
                "decision": "accepted",
                "decided_by": None,
                "deadline": None,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["decision"] == "accepted"

    async def test_create_stop_flag(self, client, mock_stop_flag_service):
        """POST /api/revisions/{id}/stop-flags — 201."""
        revision_id = uuid4()
        created = _make_stop_flag(
            id=uuid4(),
            revision_id=revision_id,
            reason="Blocking issue",
        )
        mock_stop_flag_service.create.return_value = created

        response = await client.post(
            f"/api/revisions/{revision_id}/stop-flags",
            json={
                "revision_id": str(revision_id),
                "reason": "Blocking issue",
                "resolved": False,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["reason"] == "Blocking issue"

    async def test_create_revision_invalid_version(self, client, mock_revision_service):
        """POST с version < 1 — 422."""
        document_id = uuid4()

        response = await client.post(
            f"/api/documents/{document_id}/revisions",
            json={"version": 0},
        )

        assert response.status_code == 422

    async def test_create_change_empty_field(self, client, mock_change_service):
        """POST с пустым field — 422."""
        revision_id = uuid4()

        response = await client.post(
            f"/api/revisions/{revision_id}/changes",
            json={"field": "", "status": "added", "new_value": "x"},
        )

        assert response.status_code == 422
