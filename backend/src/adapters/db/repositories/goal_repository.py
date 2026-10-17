"""SQLAlchemy-реализация GoalRepository."""

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.goal import GoalModel
from backend.src.adapters.db.models.goal_premise import GoalPremiseModel
from backend.src.domain.entities.goal import Goal
from backend.src.domain.ports.repositories import GoalRepository
from backend.src.domain.value_objects.enums import GoalState


class SqlAlchemyGoalRepository(GoalRepository):
    """Репозиторий целей на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _fetch_premise_ids(self, goal_id: UUID) -> list[UUID]:
        """Прочитать premise_ids для goal_id из goal_premises."""
        stmt = select(GoalPremiseModel.premise_id).where(
            GoalPremiseModel.goal_id == goal_id
        )
        result = await self._session.execute(stmt)
        # scalars() возвращает UUID напрямую
        return list(result.scalars().all())

    async def get_by_id(self, goal_id: UUID) -> Goal | None:
        model = await self._session.get(GoalModel, goal_id)
        if model is None:
            return None
        premise_ids = await self._fetch_premise_ids(goal_id)
        return self._to_domain(model, premise_ids=premise_ids)

    async def list_by_project(self, project_id: UUID) -> list[Goal]:
        stmt = (
            select(GoalModel)
            .where(GoalModel.project_id == project_id)
            .order_by(GoalModel.created_at.desc())
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        goals = []
        for m in models:
            premise_ids = await self._fetch_premise_ids(m.id)
            goals.append(self._to_domain(m, premise_ids=premise_ids))
        return goals

    async def save(self, goal: Goal) -> Goal:
        model = self._to_model(goal)
        merged = await self._session.merge(model)
        await self._session.flush()

        # Удаляем старые связи
        del_stmt = (
            delete(GoalPremiseModel)
            .where(GoalPremiseModel.goal_id == merged.id)
        )
        await self._session.execute(del_stmt)

        # Добавляем новые
        for premise_id in (goal.premise_ids or []):
            self._session.add(
                GoalPremiseModel(goal_id=merged.id, premise_id=premise_id)
            )

        await self._session.flush()

        # Перечитываем premise_ids напрямую
        premise_ids = await self._fetch_premise_ids(merged.id)
        return self._to_domain(merged, premise_ids=premise_ids)

    async def delete(self, goal_id: UUID) -> None:
        # Удаляем связи goal_premises (CASCADE на уровне БД)
        stmt = delete(GoalModel).where(GoalModel.id == goal_id)
        await self._session.execute(stmt)
        await self._session.flush()

    # ---------- Mapping ----------

    def _to_domain(
        self, model: GoalModel, premise_ids: list[UUID] | None = None
    ) -> Goal:
        return Goal(
            id=model.id,
            project_id=model.project_id,
            formulation=model.formulation,
            deadline=model.deadline,
            responsible_id=model.responsible_id,
            priority=model.priority,
            state=GoalState(model.state),
            created_by=model.created_by,
            premise_ids=premise_ids or [],
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
