"""Composition Root. Собирает зависимости приложения."""

from functools import lru_cache

from backend.src.config import Settings, settings
from backend.src.domain.ports.ai_port import AIPort
from backend.src.domain.ports.ai_stub import AIStub


class Container:
    """Простой DI-контейнер для MVP. Без сторонних библиотек."""

    def __init__(self, app_settings: Settings) -> None:
        self.settings = app_settings
        self._ai_port: AIPort = AIStub()

    @property
    def ai_port(self) -> AIPort:
        return self._ai_port


@lru_cache
def get_container() -> Container:
    """Singleton-контейнер."""
    return Container(settings)