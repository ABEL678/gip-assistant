"""SQLAlchemy-реализация NormRepository."""

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.norm import NormModel
from backend.src.domain.entities.norm import Norm
from backend.src.domain.ports.repositories import NormRepository
from backend.src.domain.value_objects.enums import NormType


class SqlAlchemyNormRepository(NormRepository):
    """Репозиторий норм на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, norm_id: UUID) -> Norm | None:
        model = await self._session.get(NormModel, norm_id)
        if model is None:
            return None
        return self._to_domain(model)

    async def list_by_project(self, project_id: UUID) -> list[Norm]:
        stmt = (
            select(NormModel)
            .where(NormModel.project_id == project_id)
            .order_by(NormModel.created_at.desc())
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, norm: Norm) -> Norm:
        model = self._to_model(norm)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return await self.get_by_id(merged.id)

    async def delete(self, norm_id: UUID) -> None:
        stmt = delete(NormModel).where(NormModel.id == norm_id)
        await self._session.execute(stmt)
        await self._session.flush()

    # ---------- Mapping ----------

    def _to_domain(self, model: NormModel) -> Norm:
        return Norm(
            id=model.id,
            project_id=model.project_id,
            code=model.code,
            title=model.title,
            norm_type=NormType(model.norm_type),
            issued_at=model.issued_at,
            source_url=model.source_url,
            document_id=model.document_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: Norm) -> NormModel:
        return NormModel(
            id=domain.id,
            project_id=domain.project_id,
            code=domain.code,
            title=domain.title,
            norm_type=domain.norm_type.value,
            issued_at=domain.issued_at,
            source_url=domain.source_url,
            document_id=domain.document_id,
        )
