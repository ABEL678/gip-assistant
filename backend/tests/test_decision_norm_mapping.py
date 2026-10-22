"""Smoke-тесты маппинга DecisionNormRepository."""

import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.exc import IntegrityError

from backend.src.adapters.db.repositories.decision_norm_repository import (
    SqlAlchemyDecisionNormRepository,
)


@pytest.mark.asyncio
async def test_decision_norm_link():
    """link → list_norms_by_decision возвращает UUID нормы."""
    session = AsyncMock()
    scalars_mock = MagicMock()
    scalars_mock.all.return_value = [uuid.uuid4()]
    result_mock = MagicMock()
    result_mock.scalars.return_value = scalars_mock
    session.execute = AsyncMock(return_value=result_mock)
    session.flush = AsyncMock()

    repo = SqlAlchemyDecisionNormRepository(session)
    decision_id = uuid.uuid4()
    norm_id = uuid.uuid4()

    await repo.link(decision_id, norm_id)

    norms = await repo.list_norms_by_decision(decision_id)
    assert len(norms) == 1
    assert norms[0] == scalars_mock.all.return_value[0]


@pytest.mark.asyncio
async def test_decision_norm_link_idempotent():
    """Повторный link не падает (идемпотентность)."""
    session = AsyncMock()
    session.execute = AsyncMock(side_effect=IntegrityError("", "", ""))
    session.flush = AsyncMock()
    session.rollback = AsyncMock()

    repo = SqlAlchemyDecisionNormRepository(session)
    decision_id = uuid.uuid4()
    norm_id = uuid.uuid4()

    # Не должен поднять исключение
    await repo.link(decision_id, norm_id)

    # Должен быть вызван rollback после IntegrityError
    session.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_decision_norm_unlink():
    """unlink → list_norms_by_decision возвращает пустой список."""
    session = AsyncMock()
    scalars_mock = MagicMock()
    scalars_mock.all.return_value = []
    result_mock = MagicMock()
    result_mock.scalars.return_value = scalars_mock
    session.execute = AsyncMock(return_value=result_mock)
    session.flush = AsyncMock()

    repo = SqlAlchemyDecisionNormRepository(session)
    decision_id = uuid.uuid4()
    norm_id = uuid.uuid4()

    await repo.unlink(decision_id, norm_id)

    norms = await repo.list_norms_by_decision(decision_id)
    assert norms == []


@pytest.mark.asyncio
async def test_decision_norm_list_decisions_by_norm():
    """list_decisions_by_norm возвращает UUID решений."""
    session = AsyncMock()
    norm_ids = [uuid.uuid4(), uuid.uuid4()]
    scalars_mock = MagicMock()
    scalars_mock.all.return_value = norm_ids
    result_mock = MagicMock()
    result_mock.scalars.return_value = scalars_mock
    session.execute = AsyncMock(return_value=result_mock)

    repo = SqlAlchemyDecisionNormRepository(session)
    norm_id = uuid.uuid4()

    decisions = await repo.list_decisions_by_norm(norm_id)

    assert len(decisions) == 2
    assert decisions[0] == norm_ids[0]
    assert decisions[1] == norm_ids[1]
