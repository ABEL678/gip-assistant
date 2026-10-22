"""Доменная сущность Norm (Нормативный документ)."""

from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID, uuid4

from backend.src.domain.value_objects.enums import NormType


@dataclass
class Norm:
    """Нормативный документ проекта.

    Args:
        project_id: UUID проекта.
        code: Обозначение (уникально в проекте).
        title: Название.

    Kwargs:
        norm_type: Тип нормативного документа.
        issued_at: Дата введения.
        source_url: Источник (ссылка).
        document_id: FK → documents (если есть файл).
        id: UUID нормы.
        created_at: Дата создания.
        updated_at: Дата обновления.
    """

    # Обязательные (без default)
    project_id: UUID
    code: str
    title: str
    norm_type: NormType

    # Опциональные (с default)
    issued_at: date | None = None
    source_url: str | None = None
    document_id: UUID | None = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None
