"""Адаптеры базы данных."""

from backend.src.adapters.db.base import Base, TimestampMixin

__all__ = ["Base", "TimestampMixin"]