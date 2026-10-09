"""SQLAlchemy-реализация ProjectRepository."""

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.project import Project as ProjectModel
from backend.src.domain.entities.project import Project
from backend.src.domain.ports.repositories import ProjectRepository


class SqlAlchemyProjectRepository(ProjectRepository):
    """Репозиторий проектов на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, project_id: UUID) -> Project | None:
        stmt = select(ProjectModel).where(ProjectModel.id == project_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Project]:
        stmt = select(ProjectModel).limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, project: Project) -> Project:
        model = self._to_model(project)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return self._to_domain(merged)

    async def delete(self, project_id: UUID) -> None:
        stmt = delete(ProjectModel).where(ProjectModel.id == project_id)
        await self._session.execute(stmt)
        await self._session.flush()

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: ProjectModel) -> Project:
        return Project(
            id=model.id,
            name=model.name,
            code=model.code,
            stage=model.stage,
            client=model.client,
            contract_number=model.contract_number,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: Project) -> ProjectModel:
        return ProjectModel(
            id=domain.id,
            name=domain.name,
            code=domain.code,
            stage=domain.stage,
            client=domain.client,
            contract_number=domain.contract_number,
        )