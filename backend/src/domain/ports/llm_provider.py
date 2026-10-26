"""Порт LLM-провайдера (6.14a)."""

from abc import ABC, abstractmethod
from uuid import UUID


class LLMProviderPort(ABC):
    """Контракт LLM-провайдера.

    Реализации (`QwenAdapter`, `OpenAICompatibleAdapter`,
    `RuntimeLLMAdapter`) — 6.14b.
    """

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        *,
        project_id: UUID,
    ) -> str:
        """Сгенерировать ответ.

        `project_id` обязателен: по нему проверяется светофор
        `Project.data_security_level`.
        """

    @abstractmethod
    async def health_check(self) -> bool:
        """Проверить доступность провайдера."""
