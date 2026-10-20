"""DTO — Pydantic-схемы для API."""

from backend.src.application.dto.common import ErrorResponse, Pagination
from backend.src.application.dto.cross_task import (
    CrossTaskRead,
    CrossTaskUpdate,
)
from backend.src.application.dto.import_log import (
    ImportConfirm,
    ImportLogRead,
    ImportPreview,
)
from backend.src.application.dto.project import (
    ProjectCreate,
    ProjectRead,
    ProjectUpdate,
)
from backend.src.application.dto.project_standard import (
    ProjectStandardCreate,
    ProjectStandardRead,
    ProjectStandardUpdate,
)
from backend.src.application.dto.result import (
    ResultCreate,
    ResultRead,
    ResultUpdate,
)
from backend.src.application.dto.task import (
    TaskCreate,
    TaskRead,
    TaskUpdate,
)
from backend.src.application.dto.user import UserCreate, UserRead

__all__ = [
    # Common
    "ErrorResponse",
    "Pagination",
    # Project
    "ProjectCreate",
    "ProjectRead",
    "ProjectUpdate",
    # Task
    "TaskCreate",
    "TaskRead",
    "TaskUpdate",
    # CrossTask
    "CrossTaskRead",
    "CrossTaskUpdate",
    # ImportLog
    "ImportPreview",
    "ImportConfirm",
    "ImportLogRead",
    # User
    "UserCreate",
    "UserRead",
    # Result
    "ResultCreate",
    "ResultRead",
    "ResultUpdate",
    # ProjectStandard
    "ProjectStandardCreate",
    "ProjectStandardRead",
    "ProjectStandardUpdate",
]
