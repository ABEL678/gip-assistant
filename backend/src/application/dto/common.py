"""Общие DTO-схемы."""

from pydantic import BaseModel, Field


class Pagination(BaseModel):
    """Параметры пагинации."""

    limit: int = Field(default=50, ge=1, le=500)
    offset: int = Field(default=0, ge=0)


class ErrorResponse(BaseModel):
    """Ответ с ошибкой (для OpenAPI)."""

    detail: str
    code: str | None = None