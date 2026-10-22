"""Реализации репозиториев через SQLAlchemy."""

from backend.src.adapters.db.repositories.action_repository import (
    SqlAlchemyActionRepository,
)
from backend.src.adapters.db.repositories.change_repository import (
    SqlAlchemyChangeRepository,
)
from backend.src.adapters.db.repositories.cross_task_repo import (
    SqlAlchemyCrossTaskRepository,
)
from backend.src.adapters.db.repositories.decision_link_repository import (
    SqlAlchemyDecisionLinkRepository,
)
from backend.src.adapters.db.repositories.decision_norm_repository import (
    SqlAlchemyDecisionNormRepository,
)
from backend.src.adapters.db.repositories.decision_repository import (
    SqlAlchemyDecisionRepository,
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
from backend.src.adapters.db.repositories.norm_repository import (
    SqlAlchemyNormRepository,
)
from backend.src.adapters.db.repositories.premise_repository import (
    SqlAlchemyPremiseRepository,
)
from backend.src.adapters.db.repositories.project_repo import (
    SqlAlchemyProjectRepository,
)
from backend.src.adapters.db.repositories.project_standard_repository import (
    SqlAlchemyProjectStandardRepository,
)
from backend.src.adapters.db.repositories.result_repository import (
    SqlAlchemyResultRepository,
)
from backend.src.adapters.db.repositories.revision_decision_repository import (
    SqlAlchemyRevisionDecisionRepository,
)
from backend.src.adapters.db.repositories.revision_repository import (
    SqlAlchemyRevisionRepository,
)
from backend.src.adapters.db.repositories.stop_flag_repository import (
    SqlAlchemyStopFlagRepository,
)
from backend.src.adapters.db.repositories.task_repo import (
    SqlAlchemyTaskRepository,
)
from backend.src.adapters.db.repositories.user_repo import (
    SqlAlchemyUserRepository,
)

__all__ = [
    "SqlAlchemyActionRepository",
    "SqlAlchemyChangeRepository",
    "SqlAlchemyCrossTaskRepository",
    "SqlAlchemyDecisionLinkRepository",
    "SqlAlchemyDecisionNormRepository",
    "SqlAlchemyDecisionRepository",
    "SqlAlchemyDocumentLinkRepository",
    "SqlAlchemyDocumentRepository",
    "SqlAlchemyDocumentTypeRepository",
    "SqlAlchemyDocumentVersionRepository",
    "SqlAlchemyEntityRepository",
    "SqlAlchemyEntityTypeRepository",
    "SqlAlchemyGoalRepository",
    "SqlAlchemyImportLogRepository",
    "SqlAlchemyNormRepository",
    "SqlAlchemyPremiseRepository",
    "SqlAlchemyProjectRepository",
    "SqlAlchemyProjectStandardRepository",
    "SqlAlchemyRevisionDecisionRepository",
    "SqlAlchemyRevisionRepository",
    "SqlAlchemyResultRepository",
    "SqlAlchemyStopFlagRepository",
    "SqlAlchemyTaskRepository",
    "SqlAlchemyUserRepository",
]
