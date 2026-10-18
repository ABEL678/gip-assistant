"""DTO результата валидации Goal (агент-валидатор). DOMAIN.md §4.4.1, §6.1.2."""

import uuid
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from backend.src.domain.value_objects.enums import VerificationStatus


class ValidationEvidence(BaseModel):
    """Доказательство: место в вводной, где нашлось значение."""

    model_config = ConfigDict(populate_by_name=True)

    premise_id: uuid.UUID
    field: str
    value: Any
    owner: str


class ValidationResult(BaseModel):
    """Результат проверки Goal на доказанность (spec_week_1.md §6.1.2)."""

    model_config = ConfigDict(populate_by_name=True)

    goal_id: uuid.UUID
    verification_status: VerificationStatus
    evidence: list[ValidationEvidence] = Field(default_factory=list)
    missing: list[str] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
