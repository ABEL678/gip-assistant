"""SQLAlchemy-реализация EntityRepository."""

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.entity import EntityModel
from backend.src.domain.entities.entity import Entity
from backend.src.domain.ports.repositories import EntityRepository


class SqlAlchemyEntityRepository(EntityRepository):
    """Репозиторий экземпляров сущностей на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, entity_id: UUID) -> Entity | None:
        stmt = select(EntityModel).where(EntityModel.id == entity_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_by_type(self, entity_type_id: UUID) -> list[Entity]:
        stmt = (
            select(EntityModel)
            .where(EntityModel.entity_type_id == entity_type_id)
            .order_by(EntityModel.sort_order, EntityModel.created_at)
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, entity: Entity) -> Entity:
        model = self._to_model(entity)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return self._to_domain(merged)

    async def delete(self, entity_id: UUID) -> None:
        stmt = delete(EntityModel).where(EntityModel.id == entity_id)
        await self._session.execute(stmt)
        await self._session.flush()

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: EntityModel) -> Entity:
        return Entity(
            id=model.id,
            project_id=model.project_id,
            entity_type_id=model.entity_type_id,
            data=model.data,
            sort_order=model.sort_order,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: Entity) -> EntityModel:
        return EntityModel(
            id=domain.id,
            project_id=domain.project_id,
            entity_type_id=domain.entity_type_id,
            data=domain.data,
            sort_order=domain.sort_order,
        )