"""Тесты OpenAICompatibleAdapter (6.14b)."""

import json
import logging
from uuid import uuid4

import httpx
import pytest

from backend.src.adapters.llm.openai_compatible import OpenAICompatibleAdapter
from backend.src.domain.ports.llm_provider import LLMProviderError


def _json_response(content: str = "ok") -> httpx.Response:
    return httpx.Response(
        200,
        json={"choices": [{"message": {"content": content}}]},
    )


def _make_adapter(handler, **kwargs):
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    adapter = OpenAICompatibleAdapter(
        model_name="test-model",
        base_url="https://llm.test/v1",
        client=client,
        **kwargs,
    )
    return adapter, client


@pytest.mark.asyncio
async def test_generate_posts_chat_completions():
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return _json_response()

    adapter, client = _make_adapter(handler)
    try:
        result = await adapter.generate("hello", project_id=uuid4())
    finally:
        await client.aclose()

    assert result == "ok"
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/v1/chat/completions"
    body = json.loads(requests[0].content)
    assert body["model"] == "test-model"
    assert body["messages"] == [{"role": "user", "content": "hello"}]


@pytest.mark.asyncio
async def test_generate_uses_params_and_drops_none():
    bodies: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        bodies.append(json.loads(request.content))
        return _json_response()

    adapter, client = _make_adapter(
        handler,
        params={"temperature": 0.1, "max_tokens": 32, "top_p": None},
    )
    try:
        await adapter.generate("hello", project_id=uuid4())
    finally:
        await client.aclose()

    assert bodies[0]["temperature"] == 0.1
    assert bodies[0]["max_tokens"] == 32
    assert "top_p" not in bodies[0]


@pytest.mark.asyncio
async def test_generate_sends_authorization_header():
    headers: list[httpx.Headers] = []

    def handler(request: httpx.Request) -> httpx.Response:
        headers.append(request.headers)
        return _json_response()

    adapter, client = _make_adapter(handler, api_key="secret-key")
    try:
        await adapter.generate("hello", project_id=uuid4())
    finally:
        await client.aclose()

    assert headers[0]["authorization"] == "Bearer secret-key"


@pytest.mark.asyncio
async def test_generate_without_key_has_no_authorization():
    headers: list[httpx.Headers] = []

    def handler(request: httpx.Request) -> httpx.Response:
        headers.append(request.headers)
        return _json_response()

    adapter, client = _make_adapter(handler)
    try:
        await adapter.generate("hello", project_id=uuid4())
    finally:
        await client.aclose()

    assert "authorization" not in headers[0]


@pytest.mark.asyncio
async def test_generate_non_2xx_raises():
    adapter, client = _make_adapter(lambda _: httpx.Response(500))
    try:
        with pytest.raises(LLMProviderError, match="HTTP 500"):
            await adapter.generate("hello", project_id=uuid4())
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_generate_invalid_or_empty_response_raises():
    cases = [
        lambda _: httpx.Response(200, content=b"not-json"),
        lambda _: httpx.Response(200, json={"choices": [{"message": {"content": ""}}]}),
    ]
    for handler in cases:
        adapter, client = _make_adapter(handler)
        try:
            with pytest.raises(LLMProviderError):
                await adapter.generate("hello", project_id=uuid4())
        finally:
            await client.aclose()


@pytest.mark.asyncio
async def test_generate_network_errors_raise():
    def connect_error(_: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("down")

    def read_timeout(_: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("slow")

    for handler in (connect_error, read_timeout):
        adapter, client = _make_adapter(handler)
        try:
            with pytest.raises(LLMProviderError, match="недоступен"):
                await adapter.generate("hello", project_id=uuid4())
        finally:
            await client.aclose()


@pytest.mark.asyncio
async def test_health_check_success():
    adapter, client = _make_adapter(lambda _: httpx.Response(200))
    try:
        assert await adapter.health_check() is True
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_health_check_failure_does_not_raise():
    def connect_error(_: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("down")

    for handler in (lambda _: httpx.Response(500), connect_error):
        adapter, client = _make_adapter(handler)
        try:
            assert await adapter.health_check() is False
        finally:
            await client.aclose()


@pytest.mark.asyncio
async def test_health_check_models_404_falls_back_to_chat():
    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        if request.url.path.endswith("/models"):
            return httpx.Response(404)
        return _json_response()

    adapter, client = _make_adapter(handler)
    try:
        assert await adapter.health_check() is True
    finally:
        await client.aclose()

    assert calls == ["/v1/models", "/v1/chat/completions"]


@pytest.mark.asyncio
async def test_base_url_normalization_and_validation():
    client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda _: _json_response())
    )
    adapter = OpenAICompatibleAdapter(
        model_name="m",
        base_url="https://llm.test/v1/",
        client=client,
    )
    try:
        assert adapter._base_url == "https://llm.test/v1"
    finally:
        await client.aclose()

    with pytest.raises(ValueError, match="base_url"):
        OpenAICompatibleAdapter(model_name="m", base_url="ftp://llm.test")


@pytest.mark.asyncio
async def test_client_lifecycle():
    own = OpenAICompatibleAdapter(
        model_name="m",
        base_url="https://llm.test/v1",
    )
    await own.aclose()
    assert own._client.is_closed is True

    client = httpx.AsyncClient(transport=httpx.MockTransport(lambda _: _json_response()))
    adapter = OpenAICompatibleAdapter(
        model_name="m",
        base_url="https://llm.test/v1",
        client=client,
    )
    await adapter.aclose()
    assert client.is_closed is False
    await client.aclose()


@pytest.mark.asyncio
async def test_logs_do_not_contain_prompt_key_or_response(caplog):
    caplog.set_level(logging.INFO)

    adapter, client = _make_adapter(
        lambda _: _json_response("SECRET_RESPONSE"),
        api_key="SECRET_KEY",
    )
    try:
        await adapter.generate("SECRET_PROMPT", project_id=uuid4())
    finally:
        await client.aclose()

    text = caplog.text.lower()
    assert "secret_prompt" not in text
    assert "secret_key" not in text
    assert "secret_response" not in text
    assert "authorization" not in text
