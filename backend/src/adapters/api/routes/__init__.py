"""HTTP-роуты API."""

from backend.src.adapters.api.routes.import_excel import router as import_excel_router
from backend.src.adapters.api.routes.projects import router as projects_router
from backend.src.adapters.api.routes.tasks import router as tasks_router

__all__ = [
    "import_excel_router",
    "projects_router",
    "tasks_router",
]
