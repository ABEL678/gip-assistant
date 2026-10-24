"""Pytest fixtures: моки репозиториев, тестовые данные."""

from datetime import date
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from backend.src.adapters.db.session import engine
from backend.src.domain.entities.cross_task import CrossTask
from backend.src.domain.entities.import_log import ImportLog
from backend.src.domain.entities.task import Task
from backend.src.domain.ports.repositories import (
    CrossTaskRepository,
    ImportLogRepository,
    TaskRepository,
)


@pytest.fixture(autouse=True)
def dispose_engine():
    """Очищает пул соединений engine после каждого теста.

    Предотвращает flaky-ошибки «Event loop is closed» при
    совместном запуске интеграционных тестов с реальным PostgreSQL
    (asyncpg-соединения привязаны к event loop, который закрывается
    между тестами). async dispose требует async-фикстуру, что вызывает
    предупреждение pytest-asyncio при sync teardown; sync dispose
    достаточно для сброса пула соединений.
    """
    yield
    engine.sync_engine.dispose()


@pytest.fixture
def project_id() -> UUID:
    return uuid4()


@pytest.fixture
def task_repo() -> AsyncMock:
    """Мок TaskRepository."""
    repo = AsyncMock(spec=TaskRepository)

    async def _bulk_save(tasks: list[Task]) -> list[Task]:
        for t in tasks:
            if t.id is None:
                t.id = uuid4()
        return tasks

    async def _save(task: Task) -> Task:
        if task.id is None:
            task.id = uuid4()
        return task

    repo.bulk_save.side_effect = _bulk_save
    repo.save.side_effect = _save
    repo.get_by_project.return_value = []
    return repo


@pytest.fixture
def cross_task_repo() -> AsyncMock:
    """Мок CrossTaskRepository."""
    repo = AsyncMock(spec=CrossTaskRepository)

    saved: list[CrossTask] = []

    async def _save(ct: CrossTask) -> CrossTask:
        if ct.id is None:
            ct.id = uuid4()
        saved.append(ct)
        return ct

    async def _find(project_id, from_code, to_code):
        for ct in saved:
            if (
                ct.project_id == project_id
                and ct.from_section_code == from_code
                and ct.to_section_code == to_code
            ):
                return ct
        return None

    repo.save.side_effect = _save
    repo.find.side_effect = _find
    repo.get_by_project.return_value = []
    repo._saved = saved  # для проверки в тестах
    return repo


@pytest.fixture
def import_log_repo() -> AsyncMock:
    """Мок ImportLogRepository."""
    repo = AsyncMock(spec=ImportLogRepository)

    async def _save(log: ImportLog) -> ImportLog:
        if log.id is None:
            log.id = uuid4()
        return log

    repo.save.side_effect = _save
    return repo


@pytest.fixture
def sample_rows() -> list[dict]:
    """Пример строк Excel."""
    return [
        {
            "Наименование": "Разработка ОВ",
            "Описание": "Вентиляция",
            "Срок": "2026-10-20",
            "Раздел": "ОВ",
        },
        {
            "Наименование": "Проверка АР",
            "Описание": "",
            "Срок": "15.11.2026",
            "Раздел": "АР",
        },
        {
            "Наименование": "Задание смежникам КР",
            "Описание": "Выдать",
            "Срок": date(2026, 12, 1),
            "Раздел": "КР",
        },
    ]


@pytest.fixture
def column_mapping() -> dict:
    return {
        "task_title": "Наименование",
        "description": "Описание",
        "deadline": "Срок",
        "section": "Раздел",
    }
