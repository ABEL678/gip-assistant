"""Свод протокола 2–3 прогонов (spec_week_1.md §6.3.1)."""

import uuid

from pydantic import BaseModel, ConfigDict, Field

from backend.src.domain.value_objects.enums import VerificationStatus


class ProtocolSummary(BaseModel):
    """Свод: unanimous / majority / split."""

    model_config = ConfigDict(populate_by_name=True)

    total: int
    unanimous: dict[uuid.UUID, VerificationStatus] = Field(default_factory=dict)
    majority: dict[uuid.UUID, VerificationStatus] = Field(default_factory=dict)
    split: list[uuid.UUID] = Field(default_factory=list)
