"""SQLAlchemy-реализация ImportLogRepository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.models.import_log import ImportLog as ImportLogModel
from backend.src.domain.entities.import_log import ImportLog
from backend.src.domain.ports.repositories import ImportLogRepository
from backend.src.domain.value_objects.enums import ImportStatus


class SqlAlchemyImportLogRepository(ImportLogRepository):
    """Репозиторий логов импорта Excel."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, log_id: UUID) -> ImportLog | None:
        stmt = select(ImportLogModel).where(ImportLogModel.id == log_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_by_project(self, project_id: UUID) -> list[ImportLog]:
        stmt = (
            select(ImportLogModel)
            .where(ImportLogModel.project_id == project_id)
            .order_by(ImportLogModel.imported_at.desc())
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def get_pending(self) -> ImportLog | None:
        """Взять первый лог со статусом 'parsing' (для воркера)."""
        stmt = (
            select(ImportLogModel)
            .where(ImportLogModel.status == ImportStatus.PARTIAL)
            .limit(1)
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def save(self, log: ImportLog) -> ImportLog:
        model = self._to_model(log)
        merged = await self._session.merge(model)
        await self._session.flush()
        return self._to_domain(merged)

    # ---------- Mapping ----------

    @staticmethod
    def _to_domain(model: ImportLogModel) -> ImportLog:
        return ImportLog(
            id=model.id,
            project_id=model.project_id,
            filename=model.filename,
            rows_imported=model.rows_imported,
            rows_failed=model.rows_failed,
            status=model.status,
            column_mapping=model.column_mapping,
            error_details=model.error_details,
            imported_at=model.imported_at,
        )

    @staticmethod
    def _to_model(domain: ImportLog) -> ImportLogModel:
        return ImportLogModel(
            id=domain.id,
            project_id=domain.project_id,
            filename=domain.filename,
            rows_imported=domain.rows_imported,
            rows_failed=domain.rows_failed,
            status=domain.status,
            column_mapping=domain.column_mapping,
            error_details=domain.error_details,
        )