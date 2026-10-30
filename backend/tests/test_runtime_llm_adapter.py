"""Тесты RuntimeLLMAdapter: TTL, светофор, выбор провайдера (6.14b)."""

import asyncio
from datetime import UTC, datetime
from typing import cast
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from cryptography.fernet import InvalidToken

from backend.src.adapters.llm.openai_compatible import OpenAICompatibleAdapter
from backend.src.adapters.llm.qwen import QwenAdapter
from backend.src.adapters.llm.runtime import RuntimeLLMAdapter
from backend.src.domain.entities.llm_settings import LLMSettings
from backend.src.domain.entities.project import Project
from backend.src.domain.ports.llm_provider import LLMProviderError, LLMProviderPort
from backend.src.domain.value_objects.enums import DataSecurityLevel, LLMProvider


class FakeAdapter(LLMProviderPort):
    """Фейковый провайдер для тестов диспетчера."""

    def __init__(self, response: str = "ok", health: bool = True) -> None:
        self.response = response
        self.health = health
        self.closed = False
        self.calls: list[tuple[str, str | None, object]] = []

    async def generate(self, prompt, system_prompt=None, *, project_id) -> str:
        self.calls.append((prompt, system_prompt, project_id))
        return self.response

    async def health_check(self) -> bool:
        return self.health

    async def aclose(self) -> None:
        self.closed = True


class BlockingAdapter(FakeAdapter):
    """Адаптер, удерживающий generate до сигнала."""

    def __init__(self) -> None:
        super().__init__()
        self.started = asyncio.Event()
        self.release = asyncio.Event()

    async def generate(self, prompt, system_prompt=None, *, project_id) -> str:
        self.started.set()
        await self.release.wait()
        return "ok"


def _settings(
    provider: LLMProvider = LLMProvider.QWEN,
    *,
    base_url: str | None = None,
    model_name: str = "test-model",
    params: dict | None = None,
    settings_id=None,
) -> LLMSettings:
    return LLMSettings(
        provider=provider,
        model_name=model_name,
        base_url=base_url,
        params=params or {},
        id=settings_id or uuid4(),
        updated_at=datetime.now(UTC),
    )


def _project(level: DataSecurityLevel = DataSecurityLevel.GREEN) -> Project:
    return Project(name="Test", code="TEST-001", data_security_level=level)


def _runtime(
    *,
    settings: LLMSettings | None = None,
    project: Project | None = None,
    settings_loader=None,
    key_loader=None,
    factory=None,
    clock=None,
):
    load_settings = settings_loader or AsyncMock(return_value=settings)
    load_key = key_loader or AsyncMock(return_value="secret-key")
    load_project = AsyncMock(return_value=project)
    runtime = RuntimeLLMAdapter(
        load_settings,
        load_key,
        load_project,
        ttl_seconds=60.0,
        clock=clock or (lambda: 0.0),
        adapter_factory=factory,
    )
    return runtime, load_settings, load_key, load_project


@pytest.mark.asyncio
async def test_red_cloud_blocked_before_key_and_factory():
    runtime, _, key_loader, _ = _runtime(
        settings=_settings(LLMProvider.OPENAI_COMPATIBLE, base_url="https://x"),
        project=_project(DataSecurityLevel.RED),
        factory=AsyncMock(),
    )

    with pytest.raises(ValueError, match="красной зоне"):
        await runtime.generate("prompt", project_id=uuid4())

    key_loader.assert_not_awaited()


@pytest.mark.asyncio
async def test_red_qwen_allowed():
    fake = FakeAdapter()
    runtime, _, _, _ = _runtime(
        settings=_settings(LLMProvider.QWEN),
        project=_project(DataSecurityLevel.RED),
        factory=lambda _s, _k: fake,
    )

    assert await runtime.generate("prompt", project_id=uuid4()) == "ok"


@pytest.mark.asyncio
async def test_green_cloud_allowed():
    fake = FakeAdapter()
    runtime, _, _, _ = _runtime(
        settings=_settings(LLMProvider.OPENAI_COMPATIBLE, base_url="https://x"),
        project=_project(DataSecurityLevel.GREEN),
        factory=lambda _s, _k: fake,
    )

    assert await runtime.generate("prompt", project_id=uuid4()) == "ok"


@pytest.mark.asyncio
async def test_yellow_cloud_allowed():
    fake = FakeAdapter()
    runtime, _, _, _ = _runtime(
        settings=_settings(LLMProvider.OPENAI_COMPATIBLE, base_url="https://x"),
        project=_project(DataSecurityLevel.YELLOW),
        factory=lambda _s, _k: fake,
    )

    assert await runtime.generate("prompt", project_id=uuid4()) == "ok"


@pytest.mark.asyncio
async def test_missing_project_stops_before_settings():
    settings_loader = AsyncMock()
    runtime, _, _, _ = _runtime(
        project=None,
        settings_loader=settings_loader,
        factory=AsyncMock(),
    )

    with pytest.raises(ValueError, match="не найден"):
        await runtime.generate("prompt", project_id=uuid4())

    settings_loader.assert_not_awaited()


@pytest.mark.asyncio
async def test_no_active_settings_closes_cached_adapter():
    fake = FakeAdapter()
    settings = _settings()
    settings_loader = AsyncMock(return_value=settings)
    runtime, _, _, _ = _runtime(
        settings_loader=settings_loader,
        project=_project(),
        factory=lambda _s, _k: fake,
    )

    await runtime.generate("prompt", project_id=uuid4())
    settings_loader.return_value = None

    with pytest.raises(LLMProviderError, match="не настроена"):
        await runtime.generate("prompt", project_id=uuid4())

    assert fake.closed is True


@pytest.mark.asyncio
async def test_build_adapter_qwen_fields():
    runtime, _, _, _ = _runtime()
    settings = _settings(
        LLMProvider.QWEN,
        model_name="qwen-x",
        params={"temperature": 0.1},
    )

    adapter = runtime._build_adapter(settings, "key-1234")
    try:
        assert isinstance(adapter, QwenAdapter)
        assert adapter._model_name == "qwen-x"
        assert adapter._base_url == QwenAdapter.DEFAULT_BASE_URL
        assert adapter._api_key == "key-1234"
        assert adapter._params == {"temperature": 0.1}
    finally:
        await adapter.aclose()


@pytest.mark.asyncio
async def test_build_adapter_openai_fields():
    runtime, _, _, _ = _runtime()
    settings = _settings(
        LLMProvider.OPENAI_COMPATIBLE,
        base_url="https://cloud.test/v1",
        model_name="gpt-x",
        params={"max_tokens": 10},
    )

    adapter = runtime._build_adapter(settings, "key-5678")
    try:
        assert isinstance(adapter, OpenAICompatibleAdapter)
        assert adapter._base_url == "https://cloud.test/v1"
        assert adapter._model_name == "gpt-x"
        assert adapter._api_key == "key-5678"
        assert adapter._params == {"max_tokens": 10}
    finally:
        await adapter.aclose()


@pytest.mark.asyncio
async def test_build_openai_without_base_url_raises():
    runtime, _, _, _ = _runtime()
    settings = _settings(LLMProvider.OPENAI_COMPATIBLE, base_url=None)

    with pytest.raises(LLMProviderError, match="base_url"):
        runtime._build_adapter(settings, None)


@pytest.mark.asyncio
async def test_build_qwen_without_base_url_uses_default():
    runtime, _, _, _ = _runtime()
    settings = _settings(LLMProvider.QWEN, base_url=None)

    adapter = runtime._build_adapter(settings, None)
    try:
        assert adapter._base_url == QwenAdapter.DEFAULT_BASE_URL
    finally:
        await adapter.aclose()


@pytest.mark.asyncio
async def test_api_key_passed_to_factory():
    captured: dict[str, str | None] = {}

    def factory(_settings, api_key):
        captured["key"] = api_key
        return FakeAdapter()

    runtime, _, key_loader, _ = _runtime(
        settings=_settings(),
        project=_project(),
        key_loader=AsyncMock(return_value="secret-key"),
        factory=factory,
    )

    await runtime.generate("prompt", project_id=uuid4())

    assert captured["key"] == "secret-key"
    key_loader.assert_awaited_once()


@pytest.mark.asyncio
async def test_prompt_and_return_passthrough():
    fake = FakeAdapter("answer")
    runtime, _, _, _ = _runtime(
        settings=_settings(),
        project=_project(),
        factory=lambda _s, _k: fake,
    )
    project_id = uuid4()

    result = await runtime.generate(
        "PROMPT",
        "SYSTEM",
        project_id=project_id,
    )

    assert result == "answer"
    assert fake.calls == [("PROMPT", "SYSTEM", project_id)]


@pytest.mark.asyncio
async def test_ttl_reuses_adapter():
    clock = [0.0]
    adapters: list[FakeAdapter] = []

    def factory(_settings, _key):
        adapter = FakeAdapter()
        adapters.append(adapter)
        return adapter

    runtime, _, key_loader, _ = _runtime(
        settings=_settings(),
        project=_project(),
        factory=factory,
        clock=lambda: clock[0],
    )

    await runtime.generate("one", project_id=uuid4())
    await runtime.generate("two", project_id=uuid4())

    assert len(adapters) == 1
    key_loader.assert_awaited_once()


@pytest.mark.asyncio
async def test_ttl_expiry_rebuilds_and_closes_old():
    clock = [0.0]
    adapters: list[FakeAdapter] = []

    def factory(_settings, _key):
        adapter = FakeAdapter()
        adapters.append(adapter)
        return adapter

    runtime, _, _, _ = _runtime(
        settings=_settings(),
        project=_project(),
        factory=factory,
        clock=lambda: clock[0],
    )

    await runtime.generate("one", project_id=uuid4())
    clock[0] = 61.0
    await runtime.generate("two", project_id=uuid4())

    assert len(adapters) == 2
    assert adapters[0].closed is True


@pytest.mark.asyncio
async def test_invalidate_resets_cache():
    adapters: list[FakeAdapter] = []

    def factory(_settings, _key):
        adapter = FakeAdapter()
        adapters.append(adapter)
        return adapter

    runtime, _, _, _ = _runtime(
        settings=_settings(),
        project=_project(),
        factory=factory,
    )

    await runtime.generate("one", project_id=uuid4())
    await runtime.invalidate()
    assert adapters[0].closed is True

    await runtime.generate("two", project_id=uuid4())
    assert len(adapters) == 2


@pytest.mark.asyncio
async def test_deactivate_and_settings_change_do_not_reuse_adapter():
    adapters: list[FakeAdapter] = []

    def factory(_settings, _key):
        adapter = FakeAdapter()
        adapters.append(adapter)
        return adapter

    first = _settings()
    second = _settings(settings_id=uuid4())
    settings_loader = AsyncMock(return_value=first)
    runtime, _, _, _ = _runtime(
        settings_loader=settings_loader,
        project=_project(),
        factory=factory,
    )

    await runtime.generate("one", project_id=uuid4())
    settings_loader.return_value = None
    with pytest.raises(LLMProviderError):
        await runtime.generate("two", project_id=uuid4())
    assert adapters[0].closed is True

    settings_loader.return_value = second
    await runtime.generate("three", project_id=uuid4())
    assert len(adapters) == 2


@pytest.mark.asyncio
async def test_health_check_without_settings_returns_false():
    runtime, _, _, _ = _runtime(
        settings_loader=AsyncMock(return_value=None),
        project=_project(),
    )

    assert await runtime.health_check() is False


@pytest.mark.asyncio
async def test_health_check_delegates():
    fake = FakeAdapter(health=True)
    runtime, _, _, _ = _runtime(
        settings=_settings(),
        project=_project(),
        factory=lambda _s, _k: fake,
    )

    assert await runtime.health_check() is True

    fake.health = False
    # Повторный вызов использует тот же адаптер из TTL-кэша.
    assert await runtime.health_check() is False


@pytest.mark.asyncio
async def test_health_check_build_error_returns_false():
    def factory(_settings, _key):
        raise LLMProviderError("boom")

    runtime, _, _, _ = _runtime(
        settings=_settings(),
        project=_project(),
        factory=factory,
    )

    assert await runtime.health_check() is False


@pytest.mark.asyncio
async def test_invalidate_does_not_close_in_flight_adapter():
    adapter = BlockingAdapter()
    runtime, _, _, _ = _runtime(
        settings=_settings(),
        project=_project(),
        factory=lambda _s, _k: adapter,
    )

    task = asyncio.create_task(runtime.generate("prompt", project_id=uuid4()))
    await adapter.started.wait()

    await runtime.invalidate()
    assert adapter.closed is False

    adapter.release.set()
    assert await task == "ok"
    await asyncio.sleep(0)
    assert adapter.closed is True


@pytest.mark.asyncio
async def test_loader_errors_are_wrapped():
    runtime, _, _, _ = _runtime(
        settings_loader=AsyncMock(side_effect=RuntimeError("db")),
        project=_project(),
    )
    with pytest.raises(LLMProviderError, match="настройки"):
        await runtime.generate("prompt", project_id=uuid4())

    fake = FakeAdapter()
    runtime, _, _, _ = _runtime(
        settings=_settings(),
        project=_project(),
        key_loader=AsyncMock(side_effect=InvalidToken()),
        factory=lambda _s, _k: fake,
    )
    with pytest.raises(LLMProviderError, match="ключ"):
        await runtime.generate("prompt", project_id=uuid4())

    def broken_factory(_settings, _key):
        raise ValueError("bad")

    runtime, _, _, _ = _runtime(
        settings=_settings(),
        project=_project(),
        factory=broken_factory,
    )
    with pytest.raises(LLMProviderError, match="адаптер"):
        await runtime.generate("prompt", project_id=uuid4())


@pytest.mark.asyncio
async def test_unknown_provider_raises():
    runtime, _, _, _ = _runtime()
    settings = _settings(provider=cast(LLMProvider, "unknown"))

    with pytest.raises(LLMProviderError, match="Неизвестный"):
        runtime._build_adapter(settings, None)
