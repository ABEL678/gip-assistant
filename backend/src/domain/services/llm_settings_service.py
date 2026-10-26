"""LLMSettingsService — бизнес-логика настроек LLM (6.14a)."""

import logging
from typing import Any
from uuid import UUID

from backend.src.domain.entities.llm_settings import LLMSettings
from backend.src.domain.ports.repositories import LLMSettingsRepository
from backend.src.domain.ports.secret_cipher import SecretCipherPort
from backend.src.domain.value_objects.enums import LLMProvider

logger = logging.getLogger(__name__)


class LLMSettingsService:
    """Сервис настроек LLM-провайдера."""

    def __init__(
        self,
        repo: LLMSettingsRepository,
        cipher: SecretCipherPort,
    ) -> None:
        self._repo = repo
        self._cipher = cipher

    async def list_all(self) -> list[LLMSettings]:
        """Все настройки."""
        return await self._repo.list_all()

    async def get(self, settings_id: UUID) -> LLMSettings | None:
        """Настройки по ID."""
        return await self._repo.get_by_id(settings_id)

    async def get_active(self) -> LLMSettings | None:
        """Активная настройка или None."""
        return await self._repo.get_active()

    async def create(
        self,
        provider: LLMProvider,
        model_name: str,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        params: dict[str, Any] | None = None,
        is_active: bool = False,
    ) -> LLMSettings:
        """Создать настройки.

        `api_key=""` эквивалентен `None` (ключа нет).
        """
        model_name = self._validate_model_name(model_name)
        normalized_base_url = self._normalize_base_url(base_url)
        validated_params = self._validate_params(params or {})

        encrypted: bytes | None = None
        last4: str | None = None
        if api_key is not None:
            key = api_key.strip()
            if key:
                self._validate_key(key)
                encrypted = self._cipher.encrypt(key)
                last4 = self._mask_key(key)

        if is_active:
            await self._repo.deactivate_all()

        settings = LLMSettings(
            provider=provider,
            model_name=model_name,
            base_url=normalized_base_url,
            api_key_encrypted=encrypted,
            api_key_last4=last4,
            params=validated_params,
            is_active=is_active,
        )
        saved = await self._repo.save(settings)
        logger.info("llm_settings_created id=%s", saved.id)
        return saved

    async def update(
        self,
        settings_id: UUID,
        *,
        provider: LLMProvider | None = None,
        model_name: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
        params: dict[str, Any] | None = None,
    ) -> LLMSettings:
        """Частично обновить настройки.

        `None` — не менять; `""` — очистить (base_url, api_key);
        `params={}` — заменить на пустой dict.
        """
        settings = await self._repo.get_by_id(settings_id)
        if settings is None:
            raise ValueError(f"Настройки LLM {settings_id} не найдены")

        if provider is not None:
            settings.provider = provider
        if model_name is not None:
            settings.model_name = self._validate_model_name(model_name)
        if base_url is not None:
            settings.base_url = self._normalize_base_url(base_url)
        if params is not None:
            settings.params = self._validate_params(params)
        if api_key is not None:
            key = api_key.strip()
            if key:
                self._validate_key(key)
                settings.api_key_encrypted = self._cipher.encrypt(key)
                settings.api_key_last4 = self._mask_key(key)
            else:
                settings.api_key_encrypted = None
                settings.api_key_last4 = None

        saved = await self._repo.save(settings)
        logger.info("llm_settings_updated id=%s", saved.id)
        return saved

    async def activate(self, settings_id: UUID) -> LLMSettings:
        """Сделать настройки активными (снять флаг с остальных)."""
        settings = await self._repo.get_by_id(settings_id)
        if settings is None:
            raise ValueError(f"Настройки LLM {settings_id} не найдены")

        await self._repo.deactivate_all()
        settings.is_active = True
        saved = await self._repo.save(settings)
        logger.info("llm_settings_activated id=%s", saved.id)
        return saved

    async def deactivate(self, settings_id: UUID) -> LLMSettings:
        """Снять флаг активности."""
        settings = await self._repo.get_by_id(settings_id)
        if settings is None:
            raise ValueError(f"Настройки LLM {settings_id} не найдены")

        settings.is_active = False
        saved = await self._repo.save(settings)
        logger.info("llm_settings_deactivated id=%s", saved.id)
        return saved

    async def delete(self, settings_id: UUID) -> None:
        """Удалить настройки."""
        settings = await self._repo.get_by_id(settings_id)
        if settings is None:
            raise ValueError(f"Настройки LLM {settings_id} не найдены")

        await self._repo.delete(settings_id)
        logger.info("llm_settings_deleted id=%s", settings_id)

    async def get_api_key(self, settings_id: UUID) -> str | None:
        """Расшифровать ключ для адаптера. Plaintext не логируется."""
        settings = await self._repo.get_by_id(settings_id)
        if settings is None:
            raise ValueError(f"Настройки LLM {settings_id} не найдены")
        if settings.api_key_encrypted is None:
            return None
        return self._cipher.decrypt(settings.api_key_encrypted)

    # ---------- Validation ----------

    @staticmethod
    def _validate_model_name(model_name: str) -> str:
        value = model_name.strip()
        if not value:
            raise ValueError("Название модели не может быть пустым")
        if len(value) > 100:
            raise ValueError("Название модели не может быть длиннее 100 символов")
        return value

    @staticmethod
    def _normalize_base_url(base_url: str | None) -> str | None:
        if base_url is None:
            return None
        value = base_url.strip()
        if not value:
            return None
        if len(value) > 500:
            raise ValueError("base_url не может быть длиннее 500 символов")
        if not (value.startswith("http://") or value.startswith("https://")):
            raise ValueError("base_url должен начинаться с http:// или https://")
        return value

    @staticmethod
    def _validate_key(key: str) -> None:
        if len(key) < 8:
            raise ValueError("API key too short")
        if len(key) > 1000:
            raise ValueError("api_key не может быть длиннее 1000 символов")

    @staticmethod
    def _mask_key(key: str) -> str | None:
        """Последние 4 символа — только если ключ длиннее 4."""
        return key[-4:] if len(key) > 4 else None

    @staticmethod
    def _validate_params(params: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(params, dict):
            raise ValueError("params должен быть объектом (dict)")

        result = dict(params)
        temperature = result.get("temperature")
        if temperature is not None:
            if isinstance(temperature, bool) or not isinstance(
                temperature, (int, float)
            ):
                raise ValueError("temperature должен быть числом")
            if not 0 <= temperature <= 2:
                raise ValueError("temperature должен быть в диапазоне 0..2")

        max_tokens = result.get("max_tokens")
        if max_tokens is not None:
            if isinstance(max_tokens, bool) or not isinstance(max_tokens, int):
                raise ValueError("max_tokens должен быть целым числом")
            if max_tokens <= 0:
                raise ValueError("max_tokens должен быть больше 0")

        return result
