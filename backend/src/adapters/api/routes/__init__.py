"""HTTP-роуты API."""

from backend.src.adapters.api.routes.actions import router as actions_router
from backend.src.adapters.api.routes.decision_links import (
    router as decision_links_router,
)
from backend.src.adapters.api.routes.decision_norms import (
    router as decision_norms_router,
)
from backend.src.adapters.api.routes.decisions import router as decisions_router
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
from backend.src.adapters.api.routes.goals import router as goals_router
from backend.src.adapters.api.routes.import_excel import (
    router as import_excel_router,
)
from backend.src.adapters.api.routes.matrix import router as matrix_router
from backend.src.adapters.api.routes.norms import router as norms_router
from backend.src.adapters.api.routes.premises import router as premises_router
from backend.src.adapters.api.routes.project_standards import (
    router as project_standards_router,
)
from backend.src.adapters.api.routes.projects import router as projects_router
from backend.src.adapters.api.routes.results import router as results_router
from backend.src.adapters.api.routes.revisions import router as revisions_router
from backend.src.adapters.api.routes.rfis import router as rfis_router
from backend.src.adapters.api.routes.tasks import router as tasks_router

__all__ = [
    "actions_router",
    "decision_links_router",
    "decision_norms_router",
    "decisions_router",
    "document_links_router",
    "document_types_router",
    "document_versions_router",
    "documents_router",
    "entity_types_router",
    "goals_router",
    "import_excel_router",
    "matrix_router",
    "norms_router",
    "premises_router",
    "project_standards_router",
    "projects_router",
    "revisions_router",
    "results_router",
    "rfis_router",
    "tasks_router",
]
