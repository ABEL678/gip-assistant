"""Реализации репозиториев через SQLAlchemy."""

from backend.src.adapters.db.repositories.cross_task_repo import (
    SqlAlchemyCrossTaskRepository,
)
from backend.src.adapters.db.repositories.document_link_repository import (
    SqlAlchemyDocumentLinkRepository,
)
from backend.src.adapters.db.repositories.document_repository import (
    SqlAlchemyDocumentRepository,
)
from backend.src.adapters.db.repositories.document_type_repository import (
    SqlAlchemyDocumentTypeRepository,
)
from backend.src.adapters.db.repositories.document_version_repository import (
    SqlAlchemyDocumentVersionRepository,
)
from backend.src.adapters.db.repositories.entity_repository import (
    SqlAlchemyEntityRepository,
)
from backend.src.adapters.db.repositories.entity_type_repository import (
    SqlAlchemyEntityTypeRepository,
)
from backend.src.adapters.db.repositories.goal_repository import (
    SqlAlchemyGoalRepository,
)
from backend.src.adapters.db.repositories.import_log_repo import (
    SqlAlchemyImportLogRepository,
)
from backend.src.adapters.db.repositories.premise_repository import (
    SqlAlchemyPremiseRepository,
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
    "SqlAlchemyDocumentLinkRepository",
    "SqlAlchemyDocumentRepository",
    "SqlAlchemyDocumentTypeRepository",
    "SqlAlchemyDocumentVersionRepository",
    "SqlAlchemyEntityRepository",
    "SqlAlchemyEntityTypeRepository",
    "SqlAlchemyGoalRepository",
    "SqlAlchemyImportLogRepository",
    "SqlAlchemyPremiseRepository",
    "SqlAlchemyProjectRepository",
    "SqlAlchemyTaskRepository",
    "SqlAlchemyUserRepository",
]
