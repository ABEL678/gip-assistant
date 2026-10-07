"""SQLAlchemy-реализация CrossTaskRepository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.cross_task import CrossTask as CrossTaskModel
from backend.src.domain.entities.cross_task import CrossTask
from backend.src.domain.ports.repositories import CrossTaskRepository


class SqlAlchemyCrossTaskRepository(CrossTaskRepository):
    """Репозиторий заданий смежникам."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, cross_task_id: UUID) -> CrossTask | None:
        stmt = select(CrossTaskModel).where(CrossTaskModel.id == cross_task_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_by_project(self, project_id: UUID) -> list[CrossTask]:
        stmt = (
            select(CrossTaskModel)
            .where(CrossTaskModel.project_id == project_id)
            .order_by(CrossTaskModel.from_section_code, CrossTaskModel.to_section_code)
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def find(
        self,
        project_id: UUID,
        from_section_code: str,
        to_section_code: str,
    ) -> CrossTask | None:
        stmt = select(CrossTaskModel).where(
            CrossTaskModel.project_id == project_id,
            CrossTaskModel.from_section_code == from_section_code,
            CrossTaskModel.to_section_code == to_section_code,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def save(self, cross_task: CrossTask) -> CrossTask:
        model = self._to_model(cross_task)
        merged = await self._session.merge(model)
        await self._session.flush()
        return self._to_domain(merged)

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: CrossTaskModel) -> CrossTask:
        return CrossTask(
            id=model.id,
            project_id=model.project_id,
            from_section_code=model.from_section_code,
            to_section_code=model.to_section_code,
            status=model.status,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: CrossTask) -> CrossTaskModel:
        return CrossTaskModel(
            id=domain.id,
            project_id=domain.project_id,
            from_section_code=domain.from_section_code,
            to_section_code=domain.to_section_code,
            status=domain.status,
            description=domain.description,
        )