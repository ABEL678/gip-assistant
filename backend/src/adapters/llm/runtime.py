"""Диспетчер LLM-провайдеров с TTL-кэшем и светофором (6.14b)."""

import asyncio
import logging
import time
from collections.abc import Awaitable, Callable
from datetime import datetime
from uuid import UUID

from backend.src.adapters.llm.openai_compatible import OpenAICompatibleAdapter
from backend.src.adapters.llm.qwen import QwenAdapter
from backend.src.domain.entities.llm_settings import LLMSettings
from backend.src.domain.entities.project import Project
from backend.src.domain.ports.llm_provider import LLMProviderError, LLMProviderPort
from backend.src.domain.value_objects.enums import DataSecurityLevel, LLMProvider

logger = logging.getLogger(__name__)

ActiveSettingsLoader = Callable[[], Awaitable[LLMSettings | None]]
ApiKeyLoader = Callable[[UUID], Awaitable[str | None]]
ProjectLoader = Callable[[UUID], Awaitable[Project | None]]
AdapterFactory = Callable[[LLMSettings, str | None], LLMProviderPort]


class RuntimeLLMAdapter(LLMProviderPort):
    """Выбирает активного провайдера, кэширует клиент и проверяет светофор."""

    TTL_SECONDS = 60.0

    def __init__(
        self,
        load_active_settings: ActiveSettingsLoader,
        load_api_key: ApiKeyLoader,
        load_project: ProjectLoader,
        *,
        ttl_seconds: float = TTL_SECONDS,
        clock: Callable[[], float] = time.monotonic,
        adapter_factory: AdapterFactory | None = None,
    ) -> None:
        self._load_active_settings = load_active_settings
        self._load_api_key = load_api_key
        self._load_project = load_project
        self._ttl_seconds = ttl_seconds
        self._clock = clock
        self._adapter_factory = adapter_factory or self._build_adapter

        self._adapter: LLMProviderPort | None = None
        self._cache_key: tuple[UUID, datetime | None] | None = None
        self._cached_at: float = float("-inf")
        self._in_flight: int = 0
        self._retired: list[LLMProviderPort] = []
        self._lock = asyncio.Lock()

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        *,
        project_id: UUID,
    ) -> str:
        """Сгенерировать ответ с проверкой светофора проекта."""
        project = await self._load_project_safe(project_id)
        if project is None:
            raise ValueError(f"Проект {project_id} не найден")

        settings = await self._load_active_settings_safe()
        if settings is None:
            await self._retire_current()
            raise LLMProviderError("LLM не настроена: нет активного провайдера")

        if (
            project.data_security_level is DataSecurityLevel.RED
            and settings.provider is LLMProvider.OPENAI_COMPATIBLE
        ):
            raise ValueError(
                "LLM запрещён: проект в красной зоне (data_security_level=red)"
            )

        adapter = await self._acquire_adapter(settings)
        try:
            logger.info(
                "llm_request provider=%s model=%s project_id=%s",
                settings.provider.value,
                settings.model_name,
                project_id,
            )
            return await adapter.generate(
                prompt,
                system_prompt,
                project_id=project_id,
            )
        finally:
            await self._release_adapter()

    async def health_check(self) -> bool:
        """Проверить доступность активного провайдера. Никогда не бросает."""
        try:
            settings = await self._load_active_settings_safe()
            if settings is None:
                await self._retire_current()
                return False

            adapter = await self._acquire_adapter(settings)
            try:
                return await adapter.health_check()
            finally:
                await self._release_adapter()
        except Exception:
            return False

    async def invalidate(self) -> None:
        """Сбросить кэш (после смены настроек)."""
        await self._retire_current()

    async def aclose(self) -> None:
        """Освободить ресурсы."""
        await self._retire_current()

    # ---------- Cache ----------

    async def _acquire_adapter(self, settings: LLMSettings) -> LLMProviderPort:
        cache_key = (settings.id, settings.updated_at)

        async with self._lock:
            if (
                self._adapter is not None
                and self._cache_key == cache_key
                and self._clock() - self._cached_at < self._ttl_seconds
            ):
                self._in_flight += 1
                return self._adapter

            api_key = await self._load_api_key_safe(settings.id)
            try:
                new_adapter = self._adapter_factory(settings, api_key)
            except LLMProviderError:
                raise
            except Exception as exc:
                raise LLMProviderError(
                    "Не удалось построить LLM-адаптер"
                ) from exc

            if self._adapter is not None:
                self._retired.append(self._adapter)

            self._adapter = new_adapter
            self._cache_key = cache_key
            self._cached_at = self._clock()
            self._in_flight += 1
            logger.info(
                "llm_adapter_created provider=%s model=%s settings_id=%s",
                settings.provider.value,
                settings.model_name,
                settings.id,
            )
            return new_adapter

    async def _release_adapter(self) -> None:
        async with self._lock:
            self._in_flight = max(0, self._in_flight - 1)
            retired: list[LLMProviderPort] = []
            if self._in_flight == 0 and self._retired:
                retired = self._retired
                self._retired = []

        for adapter in retired:
            await adapter.aclose()

    async def _retire_current(self) -> None:
        async with self._lock:
            if self._adapter is not None:
                self._retired.append(self._adapter)
                self._adapter = None
                self._cache_key = None
                self._cached_at = float("-inf")

            retired: list[LLMProviderPort] = []
            if self._in_flight == 0 and self._retired:
                retired = self._retired
                self._retired = []

        for adapter in retired:
            await adapter.aclose()

    # ---------- Loaders ----------

    async def _load_project_safe(self, project_id: UUID) -> Project | None:
        try:
            return await self._load_project(project_id)
        except LLMProviderError:
            raise
        except Exception as exc:
            raise LLMProviderError(
                "Не удалось загрузить проект для светофора"
            ) from exc

    async def _load_active_settings_safe(self) -> LLMSettings | None:
        try:
            return await self._load_active_settings()
        except LLMProviderError:
            raise
        except Exception as exc:
            raise LLMProviderError(
                "Не удалось загрузить настройки LLM"
            ) from exc

    async def _load_api_key_safe(self, settings_id: UUID) -> str | None:
        try:
            return await self._load_api_key(settings_id)
        except LLMProviderError:
            raise
        except Exception as exc:
            raise LLMProviderError(
                "Не удалось расшифровать API-ключ LLM"
            ) from exc

    # ---------- Factory ----------

    def _build_adapter(
        self,
        settings: LLMSettings,
        api_key: str | None,
    ) -> LLMProviderPort:
        params = {
            key: value
            for key, value in (settings.params or {}).items()
            if value is not None
        }

        if settings.provider is LLMProvider.QWEN:
            return QwenAdapter(
                model_name=settings.model_name,
                base_url=settings.base_url or QwenAdapter.DEFAULT_BASE_URL,
                api_key=api_key,
                params=params,
            )

        if settings.provider is LLMProvider.OPENAI_COMPATIBLE:
            if not settings.base_url:
                raise LLMProviderError(
                    "Для openai_compatible не задан base_url"
                )
            return OpenAICompatibleAdapter(
                model_name=settings.model_name,
                base_url=settings.base_url,
                api_key=api_key,
                params=params,
            )

        raise LLMProviderError(
            f"Неизвестный LLM-провайдер: {settings.provider}"
        )
