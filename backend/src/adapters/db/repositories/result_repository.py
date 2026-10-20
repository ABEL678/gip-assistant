"""SQLAlchemy-реализация ResultRepository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.result import ResultModel
from backend.src.adapters.db.models.result_goal import ResultGoalModel
from backend.src.domain.entities.result import Result
from backend.src.domain.ports.repositories import ResultRepository


class SqlAlchemyResultRepository(ResultRepository):
    """Репозиторий результатов на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, result_id: UUID) -> Result | None:
        model = await self._session.get(ResultModel, result_id)
        if model is None:
            return None
        return self._to_domain(model)

    async def list_by_project(self, project_id: UUID) -> list[Result]:
        stmt = select(ResultModel).where(ResultModel.project_id == project_id)
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def list_by_goal(self, goal_id: UUID) -> list[Result]:
        stmt = (
            select(ResultModel)
            .join(ResultGoalModel, ResultModel.id == ResultGoalModel.result_id)
            .where(ResultGoalModel.goal_id == goal_id)
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, result: Result) -> Result:
        model = self._to_model(result)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return self._to_domain(merged)

    async def delete(self, result_id: UUID) -> None:
        await self._session.delete(ResultModel(id=result_id))

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: ResultModel) -> Result:
        return Result(
            id=model.id,
            project_id=model.project_id,
            formulation=model.formulation,
            source=model.source,
            approved_by=model.approved_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: Result) -> ResultModel:
        return ResultModel(
            id=domain.id,
            project_id=domain.project_id,
            formulation=domain.formulation,
            source=domain.source,
            approved_by=domain.approved_by,
        )
