"""HTTP-роуты API."""

from backend.src.adapters.api.routes.document_links import (
    router as document_links_router,
)
from backend.src.adapters.api.routes.document_types import (
    router as document_types_router,
)
from backend.src.adapters.api.routes.document_versions import (
    router as document_versions_router,
)
from backend.src.adapters.api.routes.documents import router as documents_router
from backend.src.adapters.api.routes.entity_types import router as entity_types_router
from backend.src.adapters.api.routes.import_excel import (
    router as import_excel_router,
)
from backend.src.adapters.api.routes.matrix import router as matrix_router
from backend.src.adapters.api.routes.projects import router as projects_router
from backend.src.adapters.api.routes.tasks import router as tasks_router

__all__ = [
    "document_links_router",
    "document_types_router",
    "document_versions_router",
    "documents_router",
    "entity_types_router",
    "import_excel_router",
    "matrix_router",
    "projects_router",
    "tasks_router",
]
