"""Адаптер локальной Qwen (6.14b)."""

from typing import Any

import httpx

from backend.src.adapters.llm.openai_compatible import OpenAICompatibleAdapter


class QwenAdapter(OpenAICompatibleAdapter):
    """Локальная Qwen через OpenAI-совместимый endpoint (vLLM/Ollama)."""

    DEFAULT_BASE_URL = "http://localhost:8000/v1"
    DEFAULT_MODEL = "Qwen/Qwen2.5-7B-Instruct"
    provider_name = "qwen"

    def __init__(
        self,
        *,
        model_name: str = DEFAULT_MODEL,
        base_url: str = DEFAULT_BASE_URL,
        api_key: str | None = None,
        params: dict[str, Any] | None = None,
        client: httpx.AsyncClient | None = None,
        timeout: float = 60.0,
        connect_timeout: float = 5.0,
        health_timeout: float = 5.0,
    ) -> None:
        super().__init__(
            model_name=model_name,
            base_url=base_url,
            api_key=api_key,
            params=params,
            client=client,
            timeout=timeout,
            connect_timeout=connect_timeout,
            health_timeout=health_timeout,
        )
