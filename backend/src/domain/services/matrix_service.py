"""MatrixService — генерация матрицы смежников (CrossTask).

Реализация ТЗ 3.0, раздел 5.2.4.

Логика:
  Матрица строится по ФАКТИЧЕСКИМ парам (from_section → to_section)
  из задач проекта. Пустые пары — не создаются.
  Статус ячейки агрегируется по статусам задач этой пары.
"""

import logging
from datetime import date
from uuid import UUID

from backend.src.domain.entities.cross_task import CrossTask
from backend.src.domain.entities.task import Task
from backend.src.domain.ports.repositories import (
    CrossTaskRepository,
    TaskRepository,
)
from backend.src.domain.value_objects.enums import CrossTaskStatus

logger = logging.getLogger(__name__)


class MatrixService:
    """Сервис генерации матрицы смежников."""

    def __init__(
        self,
        cross_task_repo: CrossTaskRepository,
        task_repo: TaskRepository,
    ) -> None:
        self._cross_task_repo = cross_task_repo
        self._task_repo = task_repo

    async def generate_matrix(self, project_id: UUID) -> int:
        """Сгенерировать матрицу для проекта.

        Алгоритм:
        1. Загружаем ВСЕ задачи проекта.
        2. Собираем уникальные пары (from_section, to_section), где:
           - оба поля заполнены
           - from != to
        3. Для каждой пары:
           - если CrossTask уже есть — обновляем description
           - иначе создаём новую
        4. Возвращаем количество СОЗДАННЫХ ячеек.

        Args:
            project_id: UUID проекта.

        Returns:
            Количество созданных CrossTask.
        """
        # 1. Загружаем задачи (limit побольше — 5000 достаточно)
        tasks = await self._task_repo.get_by_project(project_id, limit=5000)

        if not tasks:
            logger.info("Project %s has no tasks, matrix not generated", project_id)
            return 0

        # 2. Группируем задачи по парам
        pairs: dict[tuple[str, str], list[Task]] = {}
        for t in tasks:
            from_code = t.section_code
            to_code = t.to_section_code
            if not from_code or not to_code:
                continue
            if from_code == to_code:
                continue
            pairs.setdefault((from_code, to_code), []).append(t)

        if not pairs:
            logger.info(
                "Project %s has no cross-section tasks (need section_code + to_section_code)",
                project_id,
            )
            return 0

        # 3. Создаём или обновляем CrossTask
        created = 0
        updated = 0

        for (from_section, to_section), pair_tasks in sorted(pairs.items()):
            pair_tasks_sorted = sorted(pair_tasks, key=lambda t: t.created_at or 0)
            status = _aggregate_status(pair_tasks_sorted)
            overdue_count = sum(1 for t in pair_tasks_sorted if _is_overdue(t))
            total = len(pair_tasks_sorted)
            done = sum(1 for t in pair_tasks_sorted if t.status == "DONE")

            description = (
                f"Задач: {total}, просрочено: {overdue_count}, готово: {done}"
            )

            existing = await self._cross_task_repo.find(
                project_id, from_section, to_section,
            )

            if existing:
                existing.status = status
                existing.description = description
                await self._cross_task_repo.save(existing)
                updated += 1
            else:
                cross_task = CrossTask(
                    project_id=project_id,
                    from_section_code=from_section,
                    to_section_code=to_section,
                    status=status,
                    description=description,
                )
                await self._cross_task_repo.save(cross_task)
                created += 1

        logger.info(
            "Matrix for project %s: %d pairs, created=%d, updated=%d",
            project_id,
            len(pairs),
            created,
            updated,
        )
        return created


# ---------- Helpers ----------


def _is_overdue(task: Task) -> bool:
    """Просрочена ли задача."""
    if not task.deadline:
        return False
    if task.status in ("DONE", "CANCELLED"):
        return False
    return task.deadline < date.today()


def _aggregate_status(tasks: list[Task]) -> CrossTaskStatus:
    """Агрегировать статус ячейки по статусам задач.

    Приоритет:
      1. Если все DONE → DONE
      2. Если есть REWORK → REWORK
      3. Если есть OVERDUE → OVERDUE
      4. Если есть IN_PROGRESS → IN_PROGRESS
      5. Иначе → NOT_STARTED
    """
    if not tasks:
        return CrossTaskStatus.NOT_STARTED

    statuses = [str(t.status) for t in tasks]

    # Все готовы
    if all(s == "DONE" for s in statuses):
        return CrossTaskStatus.DONE

    # Есть доработка
    if any(s == "REWORK" for s in statuses):
        return CrossTaskStatus.REWORK

    # Есть просрочка
    if any(_is_overdue(t) for t in tasks):
        return CrossTaskStatus.OVERDUE

    # Есть в работе
    if any(s == "IN_PROGRESS" for s in statuses):
        return CrossTaskStatus.IN_PROGRESS

    return CrossTaskStatus.NOT_STARTED