"""Доменная сущность DecisionLink (Связь решений)."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from backend.src.domain.value_objects.enums import DecisionLinkType


@dataclass
class DecisionLink:
    """Связь между двумя решениями проекта.

    Args:
        project_id: UUID проекта.
        from_decision_id: UUID исходного решения.
        to_decision_id: UUID целевого решения.

    Kwargs:
        link_type: Тип связи (sequential / parallel / nested).
        id: UUID связи.
        created_at: Дата создания.
    """

    # Обязательные (без default)
    project_id: UUID
    from_decision_id: UUID
    to_decision_id: UUID
    link_type: DecisionLinkType

    # Опциональные (с default)
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
