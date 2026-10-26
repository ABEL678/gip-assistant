"""Smoke-тесты маппинга LLMSettings и Project.data_security_level (6.14a)."""

import uuid
from datetime import datetime

from backend.src.adapters.db.models.llm_settings import LLMSettingsModel
from backend.src.adapters.db.models.project import Project as ProjectModel
from backend.src.adapters.db.repositories.llm_settings_repository import (
    SqlAlchemyLLMSettingsRepository,
)
from backend.src.adapters.db.repositories.project_repo import (
    SqlAlchemyProjectRepository,
)
from backend.src.domain.entities.llm_settings import LLMSettings
from backend.src.domain.entities.project import Project
from backend.src.domain.value_objects.enums import DataSecurityLevel, LLMProvider


def test_llm_settings_to_model_enum_value():
    """Domain → model: LLMProvider.QWEN становится строкой 'qwen'."""
    settings = LLMSettings(provider=LLMProvider.QWEN, model_name="qwen2.5")
    model = SqlAlchemyLLMSettingsRepository._to_model(settings)

    assert model.provider == "qwen"
    assert isinstance(model.provider, str)


def test_llm_settings_to_domain_enum_value():
    """Model → domain: строка 'openai_compatible' → LLMProvider."""
    model = LLMSettingsModel(
        id=uuid.uuid4(),
        provider="openai_compatible",
        model_name="gpt-4o",
    )
    settings = SqlAlchemyLLMSettingsRepository._to_domain(model)

    assert settings.provider is LLMProvider.OPENAI_COMPATIBLE


def test_llm_settings_all_provider_values():
    """Все значения LLMProvider маппятся корректно."""
    for enum_value in LLMProvider:
        model = LLMSettingsModel(
            id=uuid.uuid4(),
            provider=enum_value.value,
            model_name="test",
        )
        settings = SqlAlchemyLLMSettingsRepository._to_domain(model)
        assert settings.provider is enum_value


def test_llm_settings_params_preserved():
    """params (JSONB) не теряется при маппинге."""
    params = {"temperature": 0.3, "max_tokens": 2048}
    settings = LLMSettings(
        provider=LLMProvider.QWEN,
        model_name="qwen2.5",
        params=params,
    )
    model = SqlAlchemyLLMSettingsRepository._to_model(settings)
    restored = SqlAlchemyLLMSettingsRepository._to_domain(model)

    assert model.params == params
    assert restored.params == params


def test_llm_settings_key_fields_preserved():
    """api_key_encrypted (bytes) и api_key_last4 не теряются."""
    encrypted = b"fernet-ciphertext"
    settings = LLMSettings(
        provider=LLMProvider.OPENAI_COMPATIBLE,
        model_name="gpt-4o",
        api_key_encrypted=encrypted,
        api_key_last4="1234",
    )
    model = SqlAlchemyLLMSettingsRepository._to_model(settings)
    restored = SqlAlchemyLLMSettingsRepository._to_domain(model)

    assert model.api_key_encrypted == encrypted
    assert restored.api_key_encrypted == encrypted
    assert restored.api_key_last4 == "1234"


def test_project_data_security_level_to_model():
    """Domain → model: DataSecurityLevel.RED → 'red'."""
    project = Project(
        name="Test",
        code="TEST-001",
        data_security_level=DataSecurityLevel.RED,
    )
    model = SqlAlchemyProjectRepository._to_model(project)

    assert model.data_security_level == "red"


def test_project_data_security_level_to_domain():
    """Model → domain: 'yellow' → DataSecurityLevel.YELLOW."""
    model = ProjectModel(
        id=uuid.uuid4(),
        name="Test",
        code="TEST-001",
        stage="PD",
        data_security_level="yellow",
    )
    project = SqlAlchemyProjectRepository._to_domain(model)

    assert project.data_security_level is DataSecurityLevel.YELLOW


def test_llm_settings_roundtrip():
    """Domain → model → domain: все поля сохраняются, timestamps не передаются."""
    original = LLMSettings(
        provider=LLMProvider.OPENAI_COMPATIBLE,
        model_name="gpt-4o",
        base_url="https://api.example.com",
        api_key_encrypted=b"cipher",
        api_key_last4="abcd",
        params={"temperature": 0.5},
        is_active=True,
        created_at=datetime(2026, 10, 27, 12, 0, 0),
        updated_at=datetime(2026, 10, 27, 12, 0, 0),
    )
    model = SqlAlchemyLLMSettingsRepository._to_model(original)

    assert model.created_at is None
    assert model.updated_at is None

    restored = SqlAlchemyLLMSettingsRepository._to_domain(model)
    assert restored.provider is original.provider
    assert restored.model_name == original.model_name
    assert restored.base_url == original.base_url
    assert restored.api_key_encrypted == original.api_key_encrypted
    assert restored.api_key_last4 == original.api_key_last4
    assert restored.params == original.params
    assert restored.is_active is True
