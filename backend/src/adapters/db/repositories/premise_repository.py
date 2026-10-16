"""Репозиторий Premise (минимальный, для маппинга)."""

from datetime import date
from uuid import UUID

from backend.src.adapters.db.models.premise import PremiseModel
from backend.src.domain.entities.premise import Premise
from backend.src.domain.value_objects.enums import PremiseCategory


class SqlAlchemyPremiseRepository:
    """Минимальный репозиторий Premise (только маппинг для тестов)."""

    @staticmethod
    def _to_domain(model: PremiseModel) -> Premise:
        return Premise(
            id=model.id,
            project_id=model.project_id,
            category=PremiseCategory(model.category),
            name=model.name,
            source=model.source,
            date=model.date,
            actual=model.actual,
            mandatory=model.mandatory,
            link=model.link,
            valid_until=model.valid_until,
            data=model.data or {},
            schema=model.schema or {},
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: Premise) -> PremiseModel:
        return PremiseModel(
            id=domain.id,
            project_id=domain.project_id,
            category=domain.category.value,
            name=domain.name,
            source=domain.source,
            date=domain.date,
            actual=domain.actual,
            mandatory=domain.mandatory,
            link=domain.link,
            valid_until=domain.valid_until,
            data=domain.data or {},
            schema=domain.schema or {},
        )
