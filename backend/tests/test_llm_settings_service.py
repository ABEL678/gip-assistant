"""Unit-тесты LLMSettingsService (6.14a)."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from cryptography.fernet import Fernet

from backend.src.adapters.security.fernet_cipher import FernetCipher
from backend.src.domain.entities.llm_settings import LLMSettings
from backend.src.domain.ports.repositories import LLMSettingsRepository
from backend.src.domain.services.llm_settings_service import LLMSettingsService
from backend.src.domain.value_objects.enums import LLMProvider

KEY = Fernet.generate_key().decode()


async def _save(settings: LLMSettings) -> LLMSettings:
    return settings


def _service(repo: AsyncMock, key: str = KEY) -> LLMSettingsService:
    return LLMSettingsService(repo, FernetCipher(key))


def _settings(**kwargs) -> LLMSettings:
    defaults = {
        "provider": LLMProvider.QWEN,
        "model_name": "qwen2.5",
    }
    defaults.update(kwargs)
    return LLMSettings(**defaults)


@pytest.fixture
def repo() -> AsyncMock:
    repo = AsyncMock(spec=LLMSettingsRepository)
    repo.save.side_effect = _save
    return repo


@pytest.mark.asyncio
async def test_create_with_key_encrypts_and_masks(repo):
    """create: ciphertext записан, last4 = 4 символа, plaintext отсутствует."""
    service = _service(repo)

    saved = await service.create(
        LLMProvider.QWEN,
        "qwen2.5",
        api_key="secret-key-1234",
        is_active=True,
    )

    assert saved.api_key_encrypted is not None
    assert b"secret-key" not in saved.api_key_encrypted
    assert saved.api_key_last4 == "1234"
    repo.deactivate_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_without_key_or_empty_key(repo):
    """create без ключа и с api_key='' → NULL/NULL."""
    service = _service(repo)

    without_key = await service.create(LLMProvider.QWEN, "qwen2.5")
    empty_key = await service.create(LLMProvider.QWEN, "qwen2.5", api_key="")

    for settings in (without_key, empty_key):
        assert settings.api_key_encrypted is None
        assert settings.api_key_last4 is None


@pytest.mark.asyncio
async def test_create_validation_errors(repo):
    """create: пустая модель, плохой URL, temperature, max_tokens, короткий ключ."""
    service = _service(repo)

    with pytest.raises(ValueError, match="Название модели"):
        await service.create(LLMProvider.QWEN, "   ")
    with pytest.raises(ValueError, match="base_url"):
        await service.create(LLMProvider.QWEN, "qwen2.5", base_url="ftp://host")
    with pytest.raises(ValueError, match="temperature"):
        await service.create(
            LLMProvider.QWEN, "qwen2.5", params={"temperature": 3}
        )
    with pytest.raises(ValueError, match="max_tokens"):
        await service.create(
            LLMProvider.QWEN, "qwen2.5", params={"max_tokens": 0}
        )
    with pytest.raises(ValueError, match="API key too short"):
        await service.create(LLMProvider.QWEN, "qwen2.5", api_key="abc")


@pytest.mark.asyncio
async def test_update_key_semantics(repo):
    """update: None — не менять, '' — очистить, новый ключ — заменить."""
    service = _service(repo)
    original_cipher = b"old-cipher"

    repo.get_by_id.return_value = _settings(
        api_key_encrypted=original_cipher,
        api_key_last4="0000",
    )
    kept = await service.update(uuid4(), api_key=None)
    assert kept.api_key_encrypted == original_cipher
    assert kept.api_key_last4 == "0000"

    repo.get_by_id.return_value = _settings(
        api_key_encrypted=original_cipher,
        api_key_last4="0000",
    )
    cleared = await service.update(uuid4(), api_key="")
    assert cleared.api_key_encrypted is None
    assert cleared.api_key_last4 is None

    repo.get_by_id.return_value = _settings(
        api_key_encrypted=original_cipher,
        api_key_last4="0000",
    )
    replaced = await service.update(uuid4(), api_key="new-key-9999")
    assert replaced.api_key_encrypted != original_cipher
    assert replaced.api_key_last4 == "9999"


@pytest.mark.asyncio
async def test_update_fields(repo):
    """update: base_url='' и params={} очищают, provider/model_name меняются."""
    service = _service(repo)

    repo.get_by_id.return_value = _settings(
        base_url="https://old.example.com",
        params={"temperature": 0.5},
    )
    updated = await service.update(uuid4(), base_url="", params={})

    assert updated.base_url is None
    assert updated.params == {}

    repo.get_by_id.return_value = _settings()
    changed = await service.update(
        uuid4(),
        provider=LLMProvider.OPENAI_COMPATIBLE,
        model_name="  gpt-4o  ",
    )
    assert changed.provider is LLMProvider.OPENAI_COMPATIBLE
    assert changed.model_name == "gpt-4o"

    repo.get_by_id.return_value = _settings()
    with pytest.raises(ValueError, match="Название модели"):
        await service.update(uuid4(), model_name="x" * 101)


@pytest.mark.asyncio
async def test_activate_and_missing(repo):
    """activate: deactivate_all + is_active=True; нет строки → ValueError."""
    service = _service(repo)

    repo.get_by_id.return_value = _settings()
    activated = await service.activate(uuid4())

    assert activated.is_active is True
    repo.deactivate_all.assert_awaited_once()

    repo.get_by_id.return_value = None
    with pytest.raises(ValueError, match="не найдены"):
        await service.activate(uuid4())


@pytest.mark.asyncio
async def test_deactivate_and_missing(repo):
    """deactivate: is_active=False; нет строки → ValueError."""
    service = _service(repo)

    repo.get_by_id.return_value = _settings(is_active=True)
    deactivated = await service.deactivate(uuid4())

    assert deactivated.is_active is False

    repo.get_by_id.return_value = None
    with pytest.raises(ValueError, match="не найдены"):
        await service.deactivate(uuid4())


@pytest.mark.asyncio
async def test_get_active_and_list_all(repo):
    """get_active и list_all делегируют в репозиторий."""
    service = _service(repo)
    settings = _settings()

    repo.get_active.return_value = settings
    repo.list_all.return_value = [settings]

    assert await service.get_active() is settings
    assert await service.list_all() == [settings]


@pytest.mark.asyncio
async def test_get_api_key(repo):
    """get_api_key: расшифровывает, None без ключа, ValueError без строки."""
    cipher = FernetCipher(KEY)
    service = _service(repo)
    token = cipher.encrypt("abc12345")

    repo.get_by_id.return_value = _settings(api_key_encrypted=token)
    assert await service.get_api_key(uuid4()) == "abc12345"

    repo.get_by_id.return_value = _settings()
    assert await service.get_api_key(uuid4()) is None

    repo.get_by_id.return_value = None
    with pytest.raises(ValueError, match="не найдены"):
        await service.get_api_key(uuid4())


@pytest.mark.asyncio
async def test_create_without_encryption_key(repo):
    """create с ключом без LLM_ENCRYPTION_KEY → ValueError."""
    service = _service(repo, key="")

    with pytest.raises(ValueError, match="LLM_ENCRYPTION_KEY"):
        await service.create(LLMProvider.QWEN, "qwen2.5", api_key="abcdefgh")


@pytest.mark.asyncio
async def test_delete(repo):
    """delete: удаляет существующую, отсутствующая → ValueError."""
    service = _service(repo)
    settings = _settings()

    repo.get_by_id.return_value = settings
    await service.delete(settings.id)
    repo.delete.assert_awaited_once_with(settings.id)

    repo.get_by_id.return_value = None
    with pytest.raises(ValueError, match="не найдены"):
        await service.delete(uuid4())
