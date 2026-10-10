"""SQLAlchemy-реализация EntityTypeRepository."""

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.entity_type import EntityTypeModel
from backend.src.domain.entities.entity_type import EntityType
from backend.src.domain.ports.repositories import EntityTypeRepository


class SqlAlchemyEntityTypeRepository(EntityTypeRepository):
    """Репозиторий типов сущностей на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_type_id: UUID) -> EntityType | None:
        stmt = select(EntityTypeModel).where(EntityTypeModel.id == entity_type_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_by_project(self, project_id: UUID) -> list[EntityType]:
        stmt = (
            select(EntityTypeModel)
            .where(EntityTypeModel.project_id == project_id)
            .order_by(EntityTypeModel.sort_order, EntityTypeModel.created_at)
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, entity_type: EntityType) -> EntityType:
        model = self._to_model(entity_type)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return self._to_domain(merged)

    async def delete(self, entity_type_id: UUID) -> None:
        stmt = delete(EntityTypeModel).where(EntityTypeModel.id == entity_type_id)
        await self._session.execute(stmt)
        await self._session.flush()

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: EntityTypeModel) -> EntityType:
        return EntityType(
            id=model.id,
            project_id=model.project_id,
            name=model.name,
            icon=model.icon,
            color=model.color,
            description=model.description,
            field_schema=model.schema,
            is_system=model.is_system,
            sort_order=model.sort_order,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: EntityType) -> EntityTypeModel:
        return EntityTypeModel(
            id=domain.id,
            project_id=domain.project_id,
            name=domain.name,
            icon=domain.icon,
            color=domain.color,
            description=domain.description,
            schema=domain.field_schema,
            is_system=domain.is_system,
            sort_order=domain.sort_order,
        )