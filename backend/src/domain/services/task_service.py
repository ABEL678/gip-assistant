"""TaskService — бизнес-логика задач (Task)."""

import logging
from datetime import date
from uuid import UUID

from backend.src.domain.entities.task import Task
from backend.src.domain.ports.repositories import TaskRepository
from backend.src.domain.value_objects.enums import TaskStatus

logger = logging.getLogger(__name__)


class TaskService:
    """Сервис работы с задачами (Task)."""

    def __init__(self, repo: TaskRepository) -> None:
        self._repo = repo

    async def get_by_id(self, task_id: UUID) -> Task | None:
        """Найти задачу по ID.

        Args:
            task_id: UUID задачи.

        Returns:
            Задача или None.
        """
        return await self._repo.get_by_id(task_id)

    async def list_by_project(self, project_id: UUID) -> list[Task]:
        """Список задач проекта.

        Args:
            project_id: UUID проекта.

        Returns:
            Список задач.
        """
        return await self._repo.get_by_project(project_id)

    async def create(
        self,
        project_id: UUID,
        title: str,
        description: str | None = None,
        assignee_id: UUID | None = None,
        deadline: date | None = None,
        section_code: str | None = None,
        to_section_code: str | None = None,
        is_complex: bool = False,
    ) -> Task:
        """Создать задачу.

        Args:
            project_id: UUID проекта.
            title: Название задачи (не пустое).
            description: Описание.
            assignee_id: Ответственный.
            deadline: Срок выполнения.
            section_code: Код раздела-источника.
            to_section_code: Код раздела-получателя.
            is_complex: Комплексная задача.

        Raises:
            ValueError: если title пустой после strip.
        """
        title = title.strip()
        if not title:
            raise ValueError("Название задачи не может быть пустым")

        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            assignee_id=assignee_id,
            deadline=deadline,
            section_code=section_code,
            to_section_code=to_section_code,
            is_complex=is_complex,
        )
        return await self._repo.save(task)

    async def update(
        self,
        task_id: UUID,
        title: str | None = None,
        description: str | None = None,
        status: TaskStatus | None = None,
        assignee_id: UUID | None = None,
        deadline: date | None = None,
        section_code: str | None = None,
        to_section_code: str | None = None,
        sort_order: int | None = None,
        is_complex: bool | None = None,
    ) -> Task:
        """Обновить задачу.

        Args:
            task_id: UUID задачи.

        Raises:
            ValueError: если задача не найдена.
        """
        task = await self._repo.get_by_id(task_id)
        if task is None:
            raise ValueError(f"Задача {task_id} не найдена")

        if title is not None:
            title = title.strip()
            if not title:
                raise ValueError("Название задачи не может быть пустым")
            task.title = title

        if description is not None:
            task.description = description

        if status is not None:
            task.status = status

        if assignee_id is not None:
            task.assignee_id = assignee_id

        if deadline is not None:
            task.deadline = deadline

        if section_code is not None:
            task.section_code = section_code

        if to_section_code is not None:
            task.to_section_code = to_section_code

        if sort_order is not None:
            task.sort_order = sort_order

        if is_complex is not None:
            task.is_complex = is_complex

        return await self._repo.save(task)

    async def delete(self, task_id: UUID) -> None:
        """Удалить задачу.

        Raises:
            ValueError: если задача не найдена.
        """
        task = await self._repo.get_by_id(task_id)
        if task is None:
            raise ValueError(f"Задача {task_id} не найдена")

        await self._repo.delete(task_id)
