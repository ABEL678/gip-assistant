"""ActionService — бизнес-логика действий (Action)."""

import logging
from datetime import date
from uuid import UUID

from backend.src.domain.entities.action import Action
from backend.src.domain.ports.repositories import ActionRepository
from backend.src.domain.value_objects.enums import ActionState

logger = logging.getLogger(__name__)


class ActionService:
    """Сервис работы с действиями (Action)."""

    def __init__(self, repo: ActionRepository) -> None:
        self._repo = repo

    async def get_by_id(self, action_id: UUID) -> Action | None:
        """Найти действие по ID.

        Args:
            action_id: UUID действия.

        Returns:
            Действие или None.
        """
        return await self._repo.get_by_id(action_id)

    async def list_by_task(self, task_id: UUID) -> list[Action]:
        """Список действий задачи.

        Args:
            task_id: UUID задачи.

        Returns:
            Список действий.
        """
        return await self._repo.list_by_task(task_id)

    async def list_by_project(self, project_id: UUID) -> list[Action]:
        """Список действий проекта.

        Args:
            project_id: UUID проекта.

        Returns:
            Список действий.
        """
        return await self._repo.list_by_project(project_id)

    async def create(
        self,
        project_id: UUID,
        formulation: str,
        task_id: UUID | None = None,
        measurable_result: str | None = None,
        deadline: date | None = None,
        responsible_id: UUID | None = None,
        state: ActionState = ActionState.PLAN,
    ) -> Action:
        """Создать действие.

        Args:
            project_id: UUID проекта.
            formulation: Формулировка действия (не пустая).
            task_id: Связанная задача.
            measurable_result: Измеримый результат.
            deadline: Срок выполнения.
            responsible_id: Ответственный.
            state: Состояние.

        Raises:
            ValueError: если formulation пустое после strip.
        """
        formulation = formulation.strip()
        if not formulation:
            raise ValueError("Формулировка действия не может быть пустой")

        action = Action(
            project_id=project_id,
            formulation=formulation,
            task_id=task_id,
            measurable_result=measurable_result,
            deadline=deadline,
            responsible_id=responsible_id,
            state=state,
        )
        return await self._repo.save(action)

    async def update(
        self,
        action_id: UUID,
        formulation: str | None = None,
        task_id: UUID | None = None,
        measurable_result: str | None = None,
        deadline: date | None = None,
        responsible_id: UUID | None = None,
        state: ActionState | None = None,
    ) -> Action:
        """Обновить действие.

        Args:
            action_id: UUID действия.

        Raises:
            ValueError: если действие не найдено.
        """
        action = await self._repo.get_by_id(action_id)
        if action is None:
            raise ValueError(f"Действие {action_id} не найдено")

        if formulation is not None:
            formulation = formulation.strip()
            if not formulation:
                raise ValueError("Формулировка действия не может быть пустой")
            action.formulation = formulation

        if task_id is not None:
            action.task_id = task_id

        if measurable_result is not None:
            action.measurable_result = measurable_result

        if deadline is not None:
            action.deadline = deadline

        if responsible_id is not None:
            action.responsible_id = responsible_id

        if state is not None:
            action.state = state

        return await self._repo.save(action)

    async def delete(self, action_id: UUID) -> None:
        """Удалить действие.

        Raises:
            ValueError: если действие не найдено.
        """
        action = await self._repo.get_by_id(action_id)
        if action is None:
            raise ValueError(f"Действие {action_id} не найдено")

        await self._repo.delete(action_id)
