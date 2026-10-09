"""Реализации репозиториев через SQLAlchemy."""

from backend.src.adapters.db.repositories.cross_task_repo import (
    SqlAlchemyCrossTaskRepository,
)
from backend.src.adapters.db.repositories.import_log_repo import (
    SqlAlchemyImportLogRepository,
)
from backend.src.adapters.db.repositories.project_repo import (
    SqlAlchemyProjectRepository,
)
from backend.src.adapters.db.repositories.task_repo import (
    SqlAlchemyTaskRepository,
)
from backend.src.adapters.db.repositories.user_repo import (
    SqlAlchemyUserRepository,
)

__all__ = [
    "SqlAlchemyCrossTaskRepository",
    "SqlAlchemyImportLogRepository",
    "SqlAlchemyProjectRepository",
    "SqlAlchemyTaskRepository",
    "SqlAlchemyUserRepository",
]