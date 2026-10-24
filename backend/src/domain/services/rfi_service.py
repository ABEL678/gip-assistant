"""RfiService — бизнес-логика RFI (Task с is_rfi=true).

RFI — особая разновидность Task (DOMAIN.md §4.6).
CRUD через TaskRepository (save для создания/обновления).
"""

import logging
from uuid import UUID

from backend.src.domain.entities.task import Task
from backend.src.domain.ports.repositories import (
    DecisionRepository,
    GoalRepository,
    ProjectRepository,
    RfiRepository,
    TaskRepository,
)
from backend.src.domain.value_objects.enums import RfiState, TaskStatus

logger = logging.getLogger(__name__)


class RfiService:
    """Сервис работы с RFI."""

    def __init__(
        self,
        task_repo: TaskRepository,
        project_repo: ProjectRepository,
        decision_repo: DecisionRepository,
        goal_repo: GoalRepository,
        rfi_repo: RfiRepository,
    ) -> None:
        self._task_repo = task_repo
        self._project_repo = project_repo
        self._decision_repo = decision_repo
        self._goal_repo = goal_repo
        self._rfi_repo = rfi_repo

    async def create(
        self,
        project_id: UUID,
        title: str,
        rfi_cause_decision_id: UUID | None = None,
        rfi_cause_goal_id: UUID | None = None,
        rfi_due_date=None,
        rfi_state: RfiState = RfiState.OPEN,
        deadline=None,
        assignee_id: UUID | None = None,
        is_complex: bool = False,
        description: str | None = None,
    ) -> Task:
        """Создать RFI (Task с is_rfi=true).

        Args:
            project_id: UUID проекта.
            title: Название RFI.
            rfi_cause_decision_id: Причина — решение.
            rfi_cause_goal_id: Причина — цель.
            rfi_due_date: Срок ожидания ответа.
            rfi_state: Состояние RFI (по умолчанию OPEN).
            deadline: Срок выполнения.
            assignee_id: Ответственный.
            is_complex: Комплексная задача.
            description: Описание.

        Raises:
            ValueError: если валидация не пройдена.
        """
        # 1. project_id существует
        project = await self._project_repo.get_by_id(project_id)
        if project is None:
            raise ValueError(f"Проект {project_id} не найден")

        # 2. Ровно одна причина (XOR)
        has_decision = rfi_cause_decision_id is not None
        has_goal = rfi_cause_goal_id is not None
        if not (has_decision ^ has_goal):
            raise ValueError(
                "Ровно одна причина обязательна: rfi_cause_decision_id XOR rfi_cause_goal_id"
            )

        # 3. Причина из того же проекта
        if rfi_cause_decision_id is not None:
            decision = await self._decision_repo.get_by_id(rfi_cause_decision_id)
            if decision is None:
                raise ValueError(f"Решение {rfi_cause_decision_id} не найдено")
            if decision.project_id != project_id:
                raise ValueError(
                    f"Решение {rfi_cause_decision_id} принадлежит другому проекту"
                )

        if rfi_cause_goal_id is not None:
            goal = await self._goal_repo.get_by_id(rfi_cause_goal_id)
            if goal is None:
                raise ValueError(f"Цель {rfi_cause_goal_id} не найдена")
            if goal.project_id != project_id:
                raise ValueError(
                    f"Цель {rfi_cause_goal_id} принадлежит другому проекту"
                )

        # 4. is_rfi = True (выставляется сервисом)
        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            status=TaskStatus.NOT_STARTED,
            assignee_id=assignee_id,
            deadline=deadline,
            is_complex=is_complex,
            is_rfi=True,
            rfi_cause_decision_id=rfi_cause_decision_id,
            rfi_cause_goal_id=rfi_cause_goal_id,
            rfi_due_date=rfi_due_date,
            rfi_state=rfi_state,
        )
        return await self._task_repo.save(task)

    async def list_by_project(self, project_id: UUID) -> list[Task]:
        """Список RFI проекта."""
        return await self._rfi_repo.list_rfis_by_project(project_id)

    async def get(self, task_id: UUID) -> Task | None:
        """Найти RFI по ID."""
        task = await self._task_repo.get_by_id(task_id)
        if task is None or not task.is_rfi:
            return None
        return task

    async def update(
        self,
        task_id: UUID,
        *,
        title: str | None = None,
        deadline=None,
        assignee_id: UUID | None = None,
        is_complex: bool | None = None,
        rfi_cause_decision_id: UUID | None = None,
        rfi_cause_goal_id: UUID | None = None,
        rfi_due_date=None,
        rfi_state: RfiState | None = None,
    ) -> Task | None:
        """Обновить RFI.

        Примечание: None-sentinel — None означает «не менять поле».
        Для очистки rfi_cause_* нужно удалить RFI и создать заново.
        """
        task = await self._task_repo.get_by_id(task_id)
        if task is None or not task.is_rfi:
            return None

        if title is not None:
            task.title = title
        if deadline is not None:
            task.deadline = deadline
        if assignee_id is not None:
            task.assignee_id = assignee_id
        if is_complex is not None:
            task.is_complex = is_complex
        if rfi_cause_decision_id is not None:
            task.rfi_cause_decision_id = rfi_cause_decision_id
        if rfi_cause_goal_id is not None:
            task.rfi_cause_goal_id = rfi_cause_goal_id
        if rfi_due_date is not None:
            task.rfi_due_date = rfi_due_date
        if rfi_state is not None:
            task.rfi_state = rfi_state

        # Ревалидация причин после применения
        has_decision = task.rfi_cause_decision_id is not None
        has_goal = task.rfi_cause_goal_id is not None
        if not (has_decision ^ has_goal):
            raise ValueError(
                "Ровно одна причина обязательна: "
                "rfi_cause_decision_id XOR rfi_cause_goal_id"
            )

        # Проверка existence + same project для новых причин
        if rfi_cause_decision_id is not None:
            decision = await self._decision_repo.get_by_id(
                rfi_cause_decision_id
            )
            if decision is None:
                raise ValueError(
                    f"Решение {rfi_cause_decision_id} не найдено"
                )
            if decision.project_id != task.project_id:
                raise ValueError(
                    f"Решение {rfi_cause_decision_id} принадлежит другому проекту"
                )

        if rfi_cause_goal_id is not None:
            goal = await self._goal_repo.get_by_id(rfi_cause_goal_id)
            if goal is None:
                raise ValueError(f"Цель {rfi_cause_goal_id} не найдена")
            if goal.project_id != task.project_id:
                raise ValueError(
                    f"Цель {rfi_cause_goal_id} принадлежит другому проекту"
                )

        return await self._task_repo.save(task)

    async def delete(self, task_id: UUID) -> None:
        """Удалить RFI."""
        task = await self._task_repo.get_by_id(task_id)
        if task is None or not task.is_rfi:
            raise ValueError(f"RFI {task_id} не найден")
        await self._task_repo.delete(task_id)

    async def escalate(self, task_id: UUID) -> Task:
        """Эскалировать RFI (rfi_state = ESCALATED)."""
        task = await self._task_repo.get_by_id(task_id)
        if task is None or not task.is_rfi:
            raise ValueError(f"RFI {task_id} не найден")
        task.rfi_state = RfiState.ESCALATED
        return await self._task_repo.save(task)
