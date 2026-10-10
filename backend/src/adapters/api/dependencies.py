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
    SqlAlchemyEntityRepository,
    SqlAlchemyEntityTypeRepository,
    SqlAlchemyImportLogRepository,
    SqlAlchemyProjectRepository,
    SqlAlchemyTaskRepository,
)
from backend.src.adapters.db.session import AsyncSessionLocal
from backend.src.domain.ports.repositories import (
    CrossTaskRepository,
    EntityRepository,
    EntityTypeRepository,
    ImportLogRepository,
    ProjectRepository,
    TaskRepository,
)
from backend.src.domain.services import (
    EntityService,
    EntityTypeService,
    ImportService,
    MatrixService,
)

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
            await session.commit()
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


def get_entity_type_repo(session: DbSession) -> EntityTypeRepository:
    return SqlAlchemyEntityTypeRepository(session)


def get_entity_repo(session: DbSession) -> EntityRepository:
    return SqlAlchemyEntityRepository(session)


ProjectRepoDep = Annotated[ProjectRepository, Depends(get_project_repo)]
TaskRepoDep = Annotated[TaskRepository, Depends(get_task_repo)]
CrossTaskRepoDep = Annotated[CrossTaskRepository, Depends(get_cross_task_repo)]
ImportLogRepoDep = Annotated[ImportLogRepository, Depends(get_import_log_repo)]
EntityTypeRepoDep = Annotated[EntityTypeRepository, Depends(get_entity_type_repo)]
EntityRepoDep = Annotated[EntityRepository, Depends(get_entity_repo)]


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


def get_entity_type_service(
    entity_type_repo: EntityTypeRepoDep,
) -> EntityTypeService:
    return EntityTypeService(repo=entity_type_repo)


def get_entity_service(
    entity_repo: EntityRepoDep,
    entity_type_repo: EntityTypeRepoDep,
) -> EntityService:
    return EntityService(
        repo=entity_repo,
        entity_type_repo=entity_type_repo,
    )


ImportServiceDep = Annotated[ImportService, Depends(get_import_service)]
MatrixServiceDep = Annotated[MatrixService, Depends(get_matrix_service)]
EntityTypeServiceDep = Annotated[EntityTypeService, Depends(get_entity_type_service)]
EntityServiceDep = Annotated[EntityService, Depends(get_entity_service)]