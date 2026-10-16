"""Все ORM-модели (см. ТЗ 3.0, раздел 4.3)."""

from backend.src.adapters.db.models.cross_task import CrossTask
from backend.src.adapters.db.models.document import DocumentModel
from backend.src.adapters.db.models.document_link import DocumentLinkModel
from backend.src.adapters.db.models.document_type import DocumentTypeModel
from backend.src.adapters.db.models.document_version import DocumentVersionModel
from backend.src.adapters.db.models.entity import EntityModel
from backend.src.adapters.db.models.entity_type import EntityTypeModel
from backend.src.adapters.db.models.executor import Executor
from backend.src.adapters.db.models.goal import GoalModel
from backend.src.adapters.db.models.goal_premise import GoalPremiseModel
from backend.src.adapters.db.models.import_log import ImportLog
from backend.src.adapters.db.models.premise import PremiseModel
from backend.src.adapters.db.models.project import Project
from backend.src.adapters.db.models.task import Task
from backend.src.adapters.db.models.task_status_history import TaskStatusHistory
from backend.src.adapters.db.models.user import User

__all__ = [
    "CrossTask",
    "DocumentLinkModel",
    "DocumentModel",
    "DocumentTypeModel",
    "DocumentVersionModel",
    "EntityModel",
    "EntityTypeModel",
    "Executor",
    "GoalModel",
    "GoalPremiseModel",
    "ImportLog",
    "PremiseModel",
    "Project",
    "Task",
    "TaskStatusHistory",
    "User",
]
