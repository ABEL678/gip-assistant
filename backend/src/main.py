"""FastAPI-приложение ГИП-Ассистента."""

import logging

from fastapi.middleware.cors import CORSMiddleware
from fastapi_offline import FastAPIOffline

from backend.src.adapters.api.routes import (
    import_excel_router,
    matrix_router,
    projects_router,
    tasks_router,
)
from backend.src.bootstrap import get_container

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

container = get_container()
settings = container.settings

app = FastAPIOffline(
    title=settings.APP_NAME,
    version="0.1.0",
    description="GIP Assistant — backend (MVP)",
    debug=settings.APP_DEBUG,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- API routers ----------

app.include_router(projects_router)
app.include_router(import_excel_router)
app.include_router(tasks_router)
app.include_router(matrix_router)


# ---------- System routes ----------


@app.get("/api/health", tags=["system"])
async def health() -> dict:
    """Health-check."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "env": settings.APP_ENV,
    }


@app.get("/api/version", tags=["system"])
async def version() -> dict:
    """Версия API."""
    return {"version": "0.1.0", "stage": "skeleton"}


@app.get("/api/ai/ping", tags=["system"])
async def ai_ping() -> dict:
    """Проверка AI-порта (в MVP — заглушка)."""
    draft = await container.ai_port.generate_tz_draft(
        wishes=["тест"],
        project_context="test",
    )
    return {"ai_stub_response": draft}
