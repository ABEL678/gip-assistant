"""SQLAlchemy-реализация UserRepository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.user import User as UserModel
from backend.src.domain.entities.user import User
from backend.src.domain.ports.repositories import UserRepository


class SqlAlchemyUserRepository(UserRepository):
    """Репозиторий пользователей."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = select(UserModel).where(UserModel.telegram_id == telegram_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_all_with_telegram(self) -> list[User]:
        stmt = select(UserModel).where(
            UserModel.is_active.is_(True),
            UserModel.telegram_id.is_not(None),
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, user: User) -> User:
        model = self._to_model(user)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return self._to_domain(merged)

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            role=model.role,
            email=model.email,
            telegram_id=model.telegram_id,
            is_active=model.is_active,
            created_at=model.created_at,
        )

    @staticmethod
    def _to_model(domain: User) -> UserModel:
        return UserModel(
            id=domain.id,
            name=domain.name,
            role=domain.role,
            email=domain.email,
            telegram_id=domain.telegram_id,
            is_active=domain.is_active,
        )