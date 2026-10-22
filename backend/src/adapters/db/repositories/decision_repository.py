"""SQLAlchemy-реализация DecisionRepository."""

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.decision import DecisionModel
from backend.src.adapters.db.models.decision_goal import DecisionGoalModel
from backend.src.adapters.db.models.decision_premise import DecisionPremiseModel
from backend.src.domain.entities.decision import Decision
from backend.src.domain.ports.repositories import DecisionRepository
from backend.src.domain.value_objects.enums import DecisionState


class SqlAlchemyDecisionRepository(DecisionRepository):
    """Репозиторий решений на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _fetch_goal_ids(self, decision_id: UUID) -> list[UUID]:
        """Прочитать goal_ids для decision_id из decision_goals."""
        stmt = select(DecisionGoalModel.goal_id).where(
            DecisionGoalModel.decision_id == decision_id
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def _fetch_premise_ids(self, decision_id: UUID) -> list[UUID]:
        """Прочитать premise_ids для decision_id из decision_premises."""
        stmt = select(DecisionPremiseModel.premise_id).where(
            DecisionPremiseModel.decision_id == decision_id
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, decision_id: UUID) -> Decision | None:
        model = await self._session.get(DecisionModel, decision_id)
        if model is None:
            return None
        goal_ids = await self._fetch_goal_ids(decision_id)
        premise_ids = await self._fetch_premise_ids(decision_id)
        return self._to_domain(model, goal_ids=goal_ids, premise_ids=premise_ids)

    async def list_by_project(self, project_id: UUID) -> list[Decision]:
        stmt = (
            select(DecisionModel)
            .where(DecisionModel.project_id == project_id)
            .order_by(DecisionModel.created_at.desc())
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        decisions = []
        for m in models:
            goal_ids = await self._fetch_goal_ids(m.id)
            premise_ids = await self._fetch_premise_ids(m.id)
            decisions.append(
                self._to_domain(m, goal_ids=goal_ids, premise_ids=premise_ids)
            )
        return decisions

    async def save(self, decision: Decision) -> Decision:
        model = self._to_model(decision)
        merged = await self._session.merge(model)
        await self._session.flush()

        # Refresh — чтобы updated_at не был expired после merge
        await self._session.refresh(merged)

        # Синхронизация decision_goals: DELETE + INSERT
        del_goals_stmt = (
            delete(DecisionGoalModel)
            .where(DecisionGoalModel.decision_id == merged.id)
        )
        await self._session.execute(del_goals_stmt)

        for goal_id in (decision.goal_ids or []):
            self._session.add(
                DecisionGoalModel(decision_id=merged.id, goal_id=goal_id)
            )

        # Синхронизация decision_premises: DELETE + INSERT
        del_premises_stmt = (
            delete(DecisionPremiseModel)
            .where(DecisionPremiseModel.decision_id == merged.id)
        )
        await self._session.execute(del_premises_stmt)

        for premise_id in (decision.premise_ids or []):
            self._session.add(
                DecisionPremiseModel(decision_id=merged.id, premise_id=premise_id)
            )

        await self._session.flush()

        # Перечитываем через get_by_id (не возвращаем из merge!)
        return await self.get_by_id(merged.id)

    async def delete(self, decision_id: UUID) -> None:
        # CASCADE на уровне БД чистит decision_goals и decision_premises
        stmt = delete(DecisionModel).where(DecisionModel.id == decision_id)
        await self._session.execute(stmt)
        await self._session.flush()

    # ---------- Mapping ----------

    def _to_domain(
        self,
        model: DecisionModel,
        goal_ids: list[UUID] | None = None,
        premise_ids: list[UUID] | None = None,
    ) -> Decision:
        return Decision(
            id=model.id,
            project_id=model.project_id,
            formulation=model.formulation,
            rationale=model.rationale,
            context=model.context,
            deadline=model.deadline,
            state=DecisionState(model.state),
            created_by=model.created_by,
            premise_ids=premise_ids or [],
            goal_ids=goal_ids or [],
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: Decision) -> DecisionModel:
        return DecisionModel(
            id=domain.id,
            project_id=domain.project_id,
            formulation=domain.formulation,
            rationale=domain.rationale,
            context=domain.context,
            deadline=domain.deadline,
            state=domain.state.value,
            created_by=domain.created_by,
        )
