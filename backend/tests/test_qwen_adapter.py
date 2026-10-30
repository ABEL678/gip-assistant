"""Тесты QwenAdapter (6.14b)."""

import json
from uuid import uuid4

import httpx
import pytest

from backend.src.adapters.llm.qwen import QwenAdapter


def _client(handler) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


@pytest.mark.asyncio
async def test_defaults_applied():
    client = _client(lambda _: httpx.Response(200, json={}))
    adapter = QwenAdapter(client=client)
    try:
        assert adapter._base_url == "http://localhost:8000/v1"
        assert adapter._model_name == "Qwen/Qwen2.5-7B-Instruct"
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_no_api_key_by_default():
    headers: list[httpx.Headers] = []

    def handler(request: httpx.Request) -> httpx.Response:
        headers.append(request.headers)
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": "ok"}}]},
        )

    client = _client(handler)
    adapter = QwenAdapter(client=client)
    try:
        await adapter.generate("hello", project_id=uuid4())
    finally:
        await client.aclose()

    assert "authorization" not in headers[0]


@pytest.mark.asyncio
async def test_success_response_parsed():
    client = _client(
        lambda _: httpx.Response(
            200,
            json={"choices": [{"message": {"content": "qwen-ok"}}]},
        )
    )
    adapter = QwenAdapter(client=client)
    try:
        assert await adapter.generate("hello", project_id=uuid4()) == "qwen-ok"
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_custom_base_url_wins():
    bodies: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        bodies.append(json.loads(request.content))
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": "ok"}}]},
        )

    client = _client(handler)
    adapter = QwenAdapter(base_url="https://custom.test/v1/", client=client)
    try:
        await adapter.generate("hello", project_id=uuid4())
    finally:
        await client.aclose()

    assert adapter._base_url == "https://custom.test/v1"
    assert bodies[0]["model"] == "Qwen/Qwen2.5-7B-Instruct"
