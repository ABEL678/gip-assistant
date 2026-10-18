"""Поле data вводной (Premise) с владельцем (DOMAIN.md §3.4.1)."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class PremiseDataField(BaseModel):
    """Поле data вводной с владельцем.

    Если owner не указан — это «нет данных» (нельзя проверить).
    """

    model_config = ConfigDict(populate_by_name=True)

    value: Any
    owner: str | None = None
    source: str | None = None
