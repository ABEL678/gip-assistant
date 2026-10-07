"""Все ORM-модели (см. ТЗ 3.0, раздел 4.3)."""

from backend.src.adapters.db.models.cross_task import CrossTask
from backend.src.adapters.db.models.executor import Executor
from backend.src.adapters.db.models.import_log import ImportLog
from backend.src.adapters.db.models.project import Project
from backend.src.adapters.db.models.task import Task
from backend.src.adapters.db.models.task_status_history import TaskStatusHistory
from backend.src.adapters.db.models.user import User

__all__ = [
    "CrossTask",
    "Executor",
    "ImportLog",
    "Project",
    "Task",
    "TaskStatusHistory",
    "User",
]