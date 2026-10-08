"""MatrixService — генерация матрицы смежников (CrossTask).

Реализация ТЗ 3.0, раздел 5.2.4.
"""

import logging
from uuid import UUID

from backend.src.domain.entities.cross_task import CrossTask
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
        1. Собираем все разделы (уникальные section_code) из задач проекта.
        2. Для каждой пары (from_section, to_section), где from != to:
           - если CrossTask уже есть — пропускаем
           - иначе создаём со статусом NOT_STARTED.
        3. Возвращаем количество созданных ячеек.

        Args:
            project_id: UUID проекта.

        Returns:
            Количество созданных CrossTask.
        """
        # 1. Получаем задачи проекта
        tasks = await self._task_repo.get_by_project(project_id)

        # 2. Уникальные разделы (только непустые)
        sections = sorted({t.section_code for t in tasks if t.section_code})

        if len(sections) < 2:
            logger.info(
                "Project %s has only %d section(s), matrix not needed",
                project_id,
                len(sections),
            )
            return 0

        # 3. Генерируем пары
        created = 0
        for from_section in sections:
            for to_section in sections:
                if from_section == to_section:
                    continue

                existing = await self._cross_task_repo.find(project_id, from_section, to_section)
                if existing:
                    continue

                cross_task = CrossTask(
                    project_id=project_id,
                    from_section_code=from_section,
                    to_section_code=to_section,
                    status=CrossTaskStatus.NOT_STARTED,
                )
                await self._cross_task_repo.save(cross_task)
                created += 1

        logger.info(
            "Generated %d cross_tasks for project %s (%d sections)",
            created,
            project_id,
            len(sections),
        )
        return created
