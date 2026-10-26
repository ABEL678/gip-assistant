"""Интеграционные тесты llm_settings и Project.data_security_level (6.14a).

Требуют запущенный PostgreSQL и применённую миграцию
(`alembic upgrade head`). Данные откатываются в `finally`.
"""

from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from backend.src.adapters.db.repositories.llm_settings_repository import (
    SqlAlchemyLLMSettingsRepository,
)
from backend.src.adapters.db.repositories.project_repo import (
    SqlAlchemyProjectRepository,
)
from backend.src.adapters.db.session import AsyncSessionLocal
from backend.src.adapters.security.fernet_cipher import FernetCipher
from backend.src.domain.entities.llm_settings import LLMSettings
from backend.src.domain.entities.project import Project
from backend.src.domain.services.llm_settings_service import LLMSettingsService
from backend.src.domain.value_objects.enums import DataSecurityLevel, LLMProvider


@pytest.mark.asyncio
async def test_llm_settings_save_and_get():
    """save → get_by_id: enum, JSONB, bytes сохраняются."""
    async with AsyncSessionLocal() as session:
        try:
            repo = SqlAlchemyLLMSettingsRepository(session)
            settings = LLMSettings(
                provider=LLMProvider.OPENAI_COMPATIBLE,
                model_name="gpt-4o",
                base_url="https://api.example.com",
                api_key_encrypted=b"ciphertext",
                api_key_last4="1234",
                params={"temperature": 0.5, "max_tokens": 1024},
            )

            saved = await repo.save(settings)
            loaded = await repo.get_by_id(saved.id)

            assert loaded is not None
            assert loaded.provider is LLMProvider.OPENAI_COMPATIBLE
            assert loaded.model_name == "gpt-4o"
            assert loaded.base_url == "https://api.example.com"
            assert loaded.api_key_encrypted == b"ciphertext"
            assert loaded.api_key_last4 == "1234"
            assert loaded.params == {"temperature": 0.5, "max_tokens": 1024}
            assert loaded.is_active is False
        finally:
            await session.rollback()


@pytest.mark.asyncio
async def test_activate_switch_and_unique_index():
    """activate(B) снимает A; прямая активация A → IntegrityError."""
    async with AsyncSessionLocal() as session:
        try:
            repo = SqlAlchemyLLMSettingsRepository(session)
            service = LLMSettingsService(repo, FernetCipher(""))

            await repo.deactivate_all()
            first = await repo.save(
                LLMSettings(
                    provider=LLMProvider.QWEN,
                    model_name="qwen2.5",
                    is_active=True,
                )
            )
            second = await repo.save(
                LLMSettings(
                    provider=LLMProvider.OPENAI_COMPATIBLE,
                    model_name="gpt-4o",
                    is_active=False,
                )
            )

            activated = await service.activate(second.id)
            assert activated.is_active is True

            first_after = await repo.get_by_id(first.id)
            second_after = await repo.get_by_id(second.id)
            assert first_after is not None and first_after.is_active is False
            assert second_after is not None and second_after.is_active is True

            first_after.is_active = True
            with pytest.raises(IntegrityError):
                await repo.save(first_after)
        finally:
            await session.rollback()


@pytest.mark.asyncio
async def test_key_pair_check_constraint():
    """api_key_encrypted без api_key_last4 → IntegrityError."""
    async with AsyncSessionLocal() as session:
        try:
            repo = SqlAlchemyLLMSettingsRepository(session)
            settings = LLMSettings(
                provider=LLMProvider.QWEN,
                model_name="qwen2.5",
                api_key_encrypted=b"ciphertext",
                api_key_last4=None,
            )

            with pytest.raises(IntegrityError):
                await repo.save(settings)
        finally:
            await session.rollback()


@pytest.mark.asyncio
async def test_project_data_security_level_roundtrip():
    """Project с data_security_level=RED: save → get_by_id → RED."""
    async with AsyncSessionLocal() as session:
        try:
            repo = SqlAlchemyProjectRepository(session)
            project = Project(
                name="Test Security",
                code=f"SEC-{uuid4().hex[:8]}",
                data_security_level=DataSecurityLevel.RED,
            )

            saved = await repo.save(project)
            loaded = await repo.get_by_id(saved.id)

            assert loaded is not None
            assert loaded.data_security_level is DataSecurityLevel.RED
        finally:
            await session.rollback()
