"""Smoke-тесты маппинга SQLAlchemy-моделей ↔ доменных сущностей DecisionLink."""

import uuid

from backend.src.adapters.db.models.decision_link import DecisionLinkModel
from backend.src.adapters.db.repositories.decision_link_repository import (
    SqlAlchemyDecisionLinkRepository,
)
from backend.src.domain.entities.decision_link import DecisionLink
from backend.src.domain.value_objects.enums import DecisionLinkType

# Мок-репозиторий для вызова _to_domain
_mock_repo = SqlAlchemyDecisionLinkRepository.__new__(
    SqlAlchemyDecisionLinkRepository
)


def test_decision_link_to_model_enum_value():
    """Domain → model: DecisionLinkType становится строкой 'sequential'."""
    link = DecisionLink(
        project_id=uuid.uuid4(),
        from_decision_id=uuid.uuid4(),
        to_decision_id=uuid.uuid4(),
        link_type=DecisionLinkType.SEQUENTIAL,
    )
    model = SqlAlchemyDecisionLinkRepository._to_model(link)

    assert model.link_type == "sequential"
    assert isinstance(model.link_type, str)


def test_decision_link_to_domain_enum_value():
    """Model → domain: строка 'nested' превращается в DecisionLinkType.NESTED."""
    model = DecisionLinkModel(
        id=uuid.uuid4(),
        project_id=uuid.uuid4(),
        from_decision_id=uuid.uuid4(),
        to_decision_id=uuid.uuid4(),
        link_type="nested",
    )
    link = _mock_repo._to_domain(model)

    assert isinstance(link.link_type, DecisionLinkType)
    assert link.link_type == DecisionLinkType.NESTED


def test_decision_link_all_enum_values():
    """Все 3 значения DecisionLinkType маппятся корректно."""
    for enum_val in DecisionLinkType:
        model = DecisionLinkModel(
            id=uuid.uuid4(),
            project_id=uuid.uuid4(),
            from_decision_id=uuid.uuid4(),
            to_decision_id=uuid.uuid4(),
            link_type=enum_val.value,
        )
        link = _mock_repo._to_domain(model)
        assert link.link_type == enum_val


def test_decision_link_roundtrip():
    """Domain → model → domain: все поля сохраняются."""
    project_id = uuid.uuid4()
    from_id = uuid.uuid4()
    to_id = uuid.uuid4()

    link = DecisionLink(
        id=uuid.uuid4(),
        project_id=project_id,
        from_decision_id=from_id,
        to_decision_id=to_id,
        link_type=DecisionLinkType.PARALLEL,
    )
    model = SqlAlchemyDecisionLinkRepository._to_model(link)
    link2 = _mock_repo._to_domain(model)

    assert link2.project_id == project_id
    assert link2.from_decision_id == from_id
    assert link2.to_decision_id == to_id
    assert link2.link_type == DecisionLinkType.PARALLEL
