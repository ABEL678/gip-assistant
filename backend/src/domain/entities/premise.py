"""Доменная сущность Premise (Вводная)."""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any
from uuid import UUID, uuid4

from backend.src.domain.value_objects.enums import PremiseCategory
from backend.src.domain.value_objects.premise_data import PremiseDataField


@dataclass
class Premise:
    """Вводная проекта (договор, ТЗ, требования, ИД, нормы, НПА, бюрократия, внутренние).

    Args:
        project_id: UUID проекта.
        category: Категория вводной.
        name: Краткое название.

    Kwargs:
        source: Откуда пришла.
        date: Когда вступила в силу.
        actual: Актуальна (по умолчанию True).
        mandatory: Обязательна (по умолчанию True).
        link: Ссылка на документ-источник.
        valid_until: Срок действия.
        data: Типизированные поля по категории.
        schema: Схема полей для категории.
        id: UUID вводной.
        created_at: Дата создания.
        updated_at: Дата обновления.
    """

    # Обязательные (без default)
    project_id: UUID
    category: PremiseCategory
    name: str

    # Опциональные (с default)
    source: str | None = None
    date: date | None = None
    actual: bool = True
    mandatory: bool = True
    link: str | None = None
    valid_until: date | None = None
    data: dict[str, Any] = field(default_factory=dict)
    schema: dict[str, Any] = field(default_factory=dict)
    source_goal_id: UUID | None = None
    source_document_id: UUID | None = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def data_field(self, name: str) -> PremiseDataField | None:
        """Достать поле data по имени, приведя сырой dict к PremiseDataField."""
        raw = self.data.get(name)
        if raw is None:
            return None
        if isinstance(raw, PremiseDataField):
            return raw
        if isinstance(raw, dict):
            return PremiseDataField(**raw)
        return PremiseDataField(value=raw)
