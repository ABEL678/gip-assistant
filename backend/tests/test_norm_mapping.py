"""Smoke-тесты маппинга SQLAlchemy-моделей ↔ доменных сущностей Norm."""

import uuid

from backend.src.adapters.db.models.norm import NormModel
from backend.src.adapters.db.repositories.norm_repository import (
    SqlAlchemyNormRepository,
)
from backend.src.domain.entities.norm import Norm
from backend.src.domain.value_objects.enums import NormType

# Мок-репозиторий для вызова _to_domain
_mock_repo = SqlAlchemyNormRepository.__new__(SqlAlchemyNormRepository)


def test_norm_to_model_enum_value():
    """Domain → model: NormType становится строкой 'gost'."""
    norm = Norm(
        project_id=uuid.uuid4(),
        code="ГОСТ Р 21.101-2026",
        title="Основные положения",
        norm_type=NormType.GOST,
    )
    model = SqlAlchemyNormRepository._to_model(norm)

    assert model.norm_type == "gost"
    assert isinstance(model.norm_type, str)


def test_norm_to_domain_enum_value():
    """Model → domain: строка 'snip' превращается в NormType.SNIP."""
    model = NormModel(
        id=uuid.uuid4(),
        project_id=uuid.uuid4(),
        code="СНиП 1.0",
        title="Test",
        norm_type="snip",
    )
    norm = _mock_repo._to_domain(model)

    assert isinstance(norm.norm_type, NormType)
    assert norm.norm_type == NormType.SNIP


def test_norm_all_enum_values():
    """Все 5 значений NormType маппятся корректно."""
    for enum_val in NormType:
        model = NormModel(
            id=uuid.uuid4(),
            project_id=uuid.uuid4(),
            code="Test",
            title="Test",
            norm_type=enum_val.value,
        )
        norm = _mock_repo._to_domain(model)
        assert norm.norm_type == enum_val


def test_norm_roundtrip():
    """Domain → model → domain: все поля сохраняются."""
    project_id = uuid.uuid4()
    document_id = uuid.uuid4()
    from datetime import date

    norm = Norm(
        id=uuid.uuid4(),
        project_id=project_id,
        code="ГОСТ Р 21.101-2026",
        title="Основные положения по проектированию",
        norm_type=NormType.GOST,
        issued_at=date(2026, 1, 1),
        source_url="https://gost.ru/21.101",
        document_id=document_id,
    )
    model = SqlAlchemyNormRepository._to_model(norm)
    norm2 = _mock_repo._to_domain(model)

    assert norm2.project_id == project_id
    assert norm2.code == "ГОСТ Р 21.101-2026"
    assert norm2.title == "Основные положения по проектированию"
    assert norm2.norm_type == NormType.GOST
    assert norm2.issued_at == date(2026, 1, 1)
    assert norm2.source_url == "https://gost.ru/21.101"
    assert norm2.document_id == document_id
