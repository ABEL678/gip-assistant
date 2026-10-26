"""SQLAlchemy-реализация LLMSettingsRepository (6.14a)."""

from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.llm_settings import LLMSettingsModel
from backend.src.domain.entities.llm_settings import LLMSettings
from backend.src.domain.ports.repositories import LLMSettingsRepository
from backend.src.domain.value_objects.enums import LLMProvider


class SqlAlchemyLLMSettingsRepository(LLMSettingsRepository):
    """Репозиторий настроек LLM на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, settings_id: UUID) -> LLMSettings | None:
        model = await self._session.get(LLMSettingsModel, settings_id)
        if model is None:
            return None
        return self._to_domain(model)

    async def get_active(self) -> LLMSettings | None:
        stmt = (
            select(LLMSettingsModel)
            .where(LLMSettingsModel.is_active.is_(True))
            .limit(1)
        )
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        if model is None:
            return None
        return self._to_domain(model)

    async def list_all(self) -> list[LLMSettings]:
        stmt = select(LLMSettingsModel).order_by(
            LLMSettingsModel.created_at.desc()
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, settings: LLMSettings) -> LLMSettings:
        model = self._to_model(settings)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return self._to_domain(merged)

    async def delete(self, settings_id: UUID) -> None:
        stmt = delete(LLMSettingsModel).where(LLMSettingsModel.id == settings_id)
        await self._session.execute(stmt)
        await self._session.flush()

    async def deactivate_all(self) -> None:
        stmt = (
            update(LLMSettingsModel)
            .where(LLMSettingsModel.is_active.is_(True))
            .values(is_active=False)
        )
        await self._session.execute(stmt)
        await self._session.flush()

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: LLMSettingsModel) -> LLMSettings:
        return LLMSettings(
            id=model.id,
            provider=LLMProvider(model.provider),
            model_name=model.model_name,
            base_url=model.base_url,
            api_key_encrypted=model.api_key_encrypted,
            api_key_last4=model.api_key_last4,
            params=dict(model.params or {}),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(domain: LLMSettings) -> LLMSettingsModel:
        # created_at/updated_at не передаются: их заполняет TimestampMixin.
        return LLMSettingsModel(
            id=domain.id,
            provider=domain.provider.value,
            model_name=domain.model_name,
            base_url=domain.base_url,
            api_key_encrypted=domain.api_key_encrypted,
            api_key_last4=domain.api_key_last4,
            params=dict(domain.params),
            is_active=domain.is_active,
        )
