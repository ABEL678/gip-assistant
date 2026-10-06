"""Порт AI-сервисов. В MVP — заглушка (см. ТЗ 3.0, раздел 3.3)."""

from abc import ABC, abstractmethod
from uuid import UUID


class AIPort(ABC):
    """Port for AI services. Stub in MVP."""

    @abstractmethod
    async def generate_tz_draft(
        self,
        wishes: list[str],
        project_context: str,
    ) -> str:
        """Сгенерировать черновик ТЗ. В MVP не реализовано."""
        ...

    @abstractmethod
    async def analyze_risks(self, project_id: UUID) -> list[str]:
        """Проанализировать риски проекта. В MVP не реализовано."""
        ...