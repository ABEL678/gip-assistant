"""Репозиторий Goal (минимальный, для маппинга)."""

from uuid import UUID

from backend.src.adapters.db.models.goal import GoalModel
from backend.src.adapters.db.models.goal_premise import GoalPremiseModel
from backend.src.domain.entities.goal import Goal
from backend.src.domain.value_objects.enums import GoalState


class SqlAlchemyGoalRepository:
    """Минимальный репозиторий Goal (только маппинг для тестов)."""

    @staticmethod
    def _to_domain(model: GoalModel) -> Goal:
        return Goal(
            id=model.id,
            project_id=model.project_id,
            formulation=model.formulation,
            deadline=model.deadline,
            responsible_id=model.responsible_id,
            priority=model.priority,
            state=GoalState(model.state),
            created_by=model.created_by,
            premise_ids=[],
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: Goal) -> GoalModel:
        return GoalModel(
            id=domain.id,
            project_id=domain.project_id,
            formulation=domain.formulation,
            deadline=domain.deadline,
            responsible_id=domain.responsible_id,
            priority=domain.priority,
            state=domain.state.value,
            created_by=domain.created_by,
        )


class SqlAlchemyGoalPremiseRepository:
    """Минимальный репозиторий GoalPremise (только маппинг для тестов)."""

    @staticmethod
    def _to_model(goal_id: UUID, premise_id: UUID) -> GoalPremiseModel:
        return GoalPremiseModel(
            goal_id=goal_id,
            premise_id=premise_id,
        )
