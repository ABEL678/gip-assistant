"""OpenAI-compatible HTTP-адаптер LLM (6.14b)."""

import logging
import time
from typing import Any

import httpx

from backend.src.domain.ports.llm_provider import LLMProviderError, LLMProviderPort

logger = logging.getLogger(__name__)


class OpenAICompatibleAdapter(LLMProviderPort):
    """Адаптер провайдера с OpenAI-совместимым API."""

    provider_name = "openai_compatible"

    def __init__(
        self,
        *,
        model_name: str,
        base_url: str,
        api_key: str | None = None,
        params: dict[str, Any] | None = None,
        client: httpx.AsyncClient | None = None,
        timeout: float = 60.0,
        connect_timeout: float = 5.0,
        health_timeout: float = 5.0,
    ) -> None:
        if not model_name.strip():
            raise ValueError("model_name не может быть пустым")

        normalized_url = base_url.strip().rstrip("/")
        if not normalized_url.startswith(("http://", "https://")):
            raise ValueError("base_url должен начинаться с http:// или https://")

        self._model_name = model_name.strip()
        self._base_url = normalized_url
        self._api_key = api_key or None
        self._params = {
            key: value
            for key, value in (params or {}).items()
            if value is not None
        }
        self._health_timeout = health_timeout
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(
            timeout=httpx.Timeout(timeout, connect=connect_timeout)
        )

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        *,
        project_id,
    ) -> str:
        """Сгенерировать ответ через /chat/completions."""
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self._model_name,
            "messages": messages,
            "temperature": self._params.get("temperature", 0.2),
            "max_tokens": self._params.get("max_tokens", 1024),
        }

        started = time.monotonic()
        try:
            response = await self._client.post(
                f"{self._base_url}/chat/completions",
                json=payload,
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            logger.warning(
                "llm_error provider=%s status=network error=%s",
                self.provider_name,
                type(exc).__name__,
            )
            raise LLMProviderError(
                f"LLM-провайдер недоступен: {type(exc).__name__}"
            ) from exc

        if not 200 <= response.status_code < 300:
            logger.warning(
                "llm_error provider=%s status=%s",
                self.provider_name,
                response.status_code,
            )
            raise LLMProviderError(
                f"LLM-провайдер вернул HTTP {response.status_code}"
            )

        try:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            logger.warning(
                "llm_error provider=%s status=invalid_response",
                self.provider_name,
            )
            raise LLMProviderError(
                "LLM-провайдер вернул некорректный ответ"
            ) from exc

        if not isinstance(content, str) or not content.strip():
            raise LLMProviderError("LLM-провайдер вернул пустой ответ")

        logger.info(
            "llm_response provider=%s duration_ms=%d",
            self.provider_name,
            int((time.monotonic() - started) * 1000),
        )
        return content

    async def health_check(self) -> bool:
        """Проверить доступность провайдера. Никогда не бросает."""
        try:
            response = await self._client.get(
                f"{self._base_url}/models",
                headers=self._headers(),
                timeout=self._health_timeout,
            )
        except Exception:
            return False

        if 200 <= response.status_code < 300:
            return True
        if response.status_code in (404, 405):
            return await self._health_fallback()
        return False

    async def aclose(self) -> None:
        """Закрыть собственный HTTP-клиент."""
        if self._owns_client:
            await self._client.aclose()

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        return headers

    async def _health_fallback(self) -> bool:
        """Минимальный chat-completion для шлюзов без /models."""
        payload = {
            "model": self._model_name,
            "messages": [{"role": "user", "content": "ping"}],
            "temperature": 0,
            "max_tokens": 1,
        }
        try:
            response = await self._client.post(
                f"{self._base_url}/chat/completions",
                json=payload,
                headers=self._headers(),
                timeout=self._health_timeout,
            )
        except Exception:
            return False
        return 200 <= response.status_code < 300
