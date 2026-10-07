"""Абстрактные интерфейсы репозиториев (порты).

Домен общается с БД через эти интерфейсы.
Реализации — в backend.src.adapters.db.repositories.
"""

from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from backend.src.domain.entities.cross_task import CrossTask
from backend.src.domain.entities.import_log import ImportLog
from backend.src.domain.entities.project import Project
from backend.src.domain.entities.task import Task


class ProjectRepository(ABC):
    """Репозиторий проектов."""

    @abstractmethod
    async def get_by_id(self, project_id: UUID) -> Project | None:
        ...

    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Project]:
        ...

    @abstractmethod
    async def save(self, project: Project) -> Project:
        ...

    @abstractmethod
    async def delete(self, project_id: UUID) -> None:
        ...


class TaskRepository(ABC):
    """Репозиторий задач."""

    @abstractmethod
    async def get_by_id(self, task_id: UUID) -> Task | None:
        ...

    @abstractmethod
    async def get_by_project(
        self, project_id: UUID, limit: int = 500, offset: int = 0
    ) -> list[Task]:
        ...

    @abstractmethod
    async def get_overdue(self, as_of: date | None = None) -> list[Task]:
        ...

    @abstractmethod
    async def get_upcoming(self, days: int = 3) -> list[Task]:
        ...

    @abstractmethod
    async def save(self, task: Task) -> Task:
        ...

    @abstractmethod
    async def bulk_save(self, tasks: list[Task]) -> list[Task]:
        ...

    @abstractmethod
    async def delete(self, task_id: UUID) -> None:
        ...


class CrossTaskRepository(ABC):
    """Репозиторий заданий смежникам (ячейки матрицы)."""

    @abstractmethod
    async def get_by_id(self, cross_task_id: UUID) -> CrossTask | None:
        ...

    @abstractmethod
    async def get_by_project(self, project_id: UUID) -> list[CrossTask]:
        ...

    @abstractmethod
    async def find(
        self,
        project_id: UUID,
        from_section_code: str,
        to_section_code: str,
    ) -> CrossTask | None:
        ...

    @abstractmethod
    async def save(self, cross_task: CrossTask) -> CrossTask:
        ...


class ImportLogRepository(ABC):
    """Репозиторий логов импорта Excel."""

    @abstractmethod
    async def get_by_id(self, log_id: UUID) -> ImportLog | None:
        ...

    @abstractmethod
    async def get_by_project(self, project_id: UUID) -> list[ImportLog]:
        ...

    @abstractmethod
    async def get_pending(self) -> ImportLog | None:
        """Взять первый лог со статусом 'parsing' для воркера."""
        ...

    @abstractmethod
    async def save(self, log: ImportLog) -> ImportLog:
        ...