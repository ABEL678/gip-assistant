"""FastAPI dependencies (DI через Depends).

Здесь мы связываем:
- SQLAlchemy-сессию (adapter/db)
- Репозитории (adapter/db/repositories)
- Доменные сервисы (domain/services)

И передаём их в роуты через `Depends`.
"""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.repositories import (
    SqlAlchemyCrossTaskRepository,
    SqlAlchemyImportLogRepository,
    SqlAlchemyProjectRepository,
    SqlAlchemyTaskRepository,
)
from backend.src.adapters.db.session import AsyncSessionLocal
from backend.src.domain.ports.repositories import (
    CrossTaskRepository,
    ImportLogRepository,
    ProjectRepository,
    TaskRepository,
)
from backend.src.domain.services import ImportService, MatrixService

# ---------- Session ----------


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Открыть сессию БД на время запроса.

    После успешного запроса — commit.
    При ошибке — rollback.
    Сессия автоматически закроется (async with).
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()          # ← НОВАЯ СТРОКА
        except Exception:
            await session.rollback()
            raise


DbSession = Annotated[AsyncSession, Depends(get_db_session)]


# ---------- Repositories ----------


def get_project_repo(session: DbSession) -> ProjectRepository:
    return SqlAlchemyProjectRepository(session)


def get_task_repo(session: DbSession) -> TaskRepository:
    return SqlAlchemyTaskRepository(session)


def get_cross_task_repo(session: DbSession) -> CrossTaskRepository:
    return SqlAlchemyCrossTaskRepository(session)


def get_import_log_repo(session: DbSession) -> ImportLogRepository:
    return SqlAlchemyImportLogRepository(session)


ProjectRepoDep = Annotated[ProjectRepository, Depends(get_project_repo)]
TaskRepoDep = Annotated[TaskRepository, Depends(get_task_repo)]
CrossTaskRepoDep = Annotated[CrossTaskRepository, Depends(get_cross_task_repo)]
ImportLogRepoDep = Annotated[ImportLogRepository, Depends(get_import_log_repo)]


# ---------- Domain services ----------


def get_import_service(
    task_repo: TaskRepoDep,
    import_log_repo: ImportLogRepoDep,
) -> ImportService:
    return ImportService(
        task_repo=task_repo,
        import_log_repo=import_log_repo,
    )


def get_matrix_service(
    cross_task_repo: CrossTaskRepoDep,
    task_repo: TaskRepoDep,
) -> MatrixService:
    return MatrixService(
        cross_task_repo=cross_task_repo,
        task_repo=task_repo,
    )


ImportServiceDep = Annotated[ImportService, Depends(get_import_service)]
MatrixServiceDep = Annotated[MatrixService, Depends(get_matrix_service)]
