"""Smoke-тесты маппинга SQLAlchemy-моделей ↔ доменных сущностей Premise."""

import uuid

from backend.src.adapters.db.models.premise import PremiseModel
from backend.src.adapters.db.repositories.premise_repository import (
    SqlAlchemyPremiseRepository,
)
from backend.src.domain.entities.premise import Premise
from backend.src.domain.value_objects.enums import PremiseCategory


def test_premise_to_model_enum_value():
    """Domain → model: PremiseCategory становится строкой 'contract'."""
    premise = Premise(
        project_id=uuid.uuid4(),
        category=PremiseCategory.CONTRACT,
        name="Договор на разработку",
    )
    model = SqlAlchemyPremiseRepository._to_model(premise)

    assert model.category == "contract"
    assert isinstance(model.category, str)


def test_premise_to_domain_enum_value():
    """Model → domain: строка 'tz' превращается в PremiseCategory.TZ."""
    model = PremiseModel(
        id=uuid.uuid4(),
        project_id=uuid.uuid4(),
        category="tz",
        name="Техническое задание",
    )
    premise = SqlAlchemyPremiseRepository._to_domain(model)

    assert isinstance(premise.category, PremiseCategory)
    assert premise.category == PremiseCategory.TZ


def test_premise_roundtrip():
    """Domain → model → domain: все поля сохраняются."""
    project_id = uuid.uuid4()
    premise_id = uuid.uuid4()
    premise = Premise(
        id=premise_id,
        project_id=project_id,
        category=PremiseCategory.CUSTOMER_REQUIREMENT,
        name="Требование ускориться",
        source="Письмо Заказчика №12",
        actual=True,
        mandatory=False,
        link="http://example.com/letter",
    )
    model = SqlAlchemyPremiseRepository._to_model(premise)
    premise2 = SqlAlchemyPremiseRepository._to_domain(model)

    assert premise2.id == premise_id
    assert premise2.project_id == project_id
    assert premise2.category == PremiseCategory.CUSTOMER_REQUIREMENT
    assert premise2.name == "Требование ускориться"
    assert premise2.source == "Письмо Заказчика №12"
    assert premise2.actual is True
    assert premise2.mandatory is False
    assert premise2.link == "http://example.com/letter"


def test_premise_jsonb_fields():
    """Domain → model → domain: JSONB-поля data и schema сохраняются."""
    project_id = uuid.uuid4()
    premise = Premise(
        id=uuid.uuid4(),
        project_id=project_id,
        category=PremiseCategory.SOURCE_DATA,
        name="Грунтовые условия",
        data={"ground_level": 15.5, "soil_type": "clay"},
        schema={"ground_level": "float", "soil_type": "string"},
    )
    model = SqlAlchemyPremiseRepository._to_model(premise)
    premise2 = SqlAlchemyPremiseRepository._to_domain(model)

    assert premise2.data == {"ground_level": 15.5, "soil_type": "clay"}
    assert premise2.schema == {"ground_level": "float", "soil_type": "string"}
