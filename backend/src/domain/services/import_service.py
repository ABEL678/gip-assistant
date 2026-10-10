"""ImportService — импорт задач из Excel-строк.

Реализация ТЗ 3.0, раздел 5.1.4.

ВАЖНО: ImportService не читает Excel. Он принимает УЖЕ РАСПАРСЕННЫЕ строки
(list[dict]) + column_mapping. Парсинг Excel — задача адаптера
(backend.src.adapters.import_export.excel_parser) или API-роута.
"""

import logging
from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from backend.src.domain.entities.import_log import ImportLog
from backend.src.domain.entities.task import Task
from backend.src.domain.ports.repositories import (
    ImportLogRepository,
    TaskRepository,
)
from backend.src.domain.value_objects.enums import ImportStatus, TaskStatus

logger = logging.getLogger(__name__)


@dataclass
class ImportError:
    """Ошибка одной строки при импорте."""

    row: int
    message: str


@dataclass
class ImportResult:
    """Результат импорта."""

    tasks_created: int
    errors: list[ImportError]
    log_id: UUID


class ImportService:
    """Сервис импорта задач из Excel-строк."""

    def __init__(
        self,
        task_repo: TaskRepository,
        import_log_repo: ImportLogRepository,
    ) -> None:
        self._task_repo = task_repo
        self._import_log_repo = import_log_repo

    async def import_excel(
        self,
        project_id: UUID,
        rows: list[dict],
        column_mapping: dict,
        filename: str | None = None,
    ) -> ImportResult:
        """Импортировать строки Excel в задачи проекта.

        Args:
            project_id: UUID проекта, куда импортируем.
            rows: Список словарей (строк Excel).
            column_mapping: Маппинг колонок, например:
                {
                    "task_title": "Наименование",
                    "description": "Описание",
                    "deadline": "Срок",
                    "section": "дисциплина",
                    "to_section": "кому",
                    "assignee": "Исполнитель",
                }
            filename: Имя исходного файла (для лога).

        Returns:
            ImportResult с количеством созданных задач и ошибками.
        """
        tasks: list[Task] = []
        errors: list[ImportError] = []

        for i, row in enumerate(rows):
            try:
                task = self._row_to_task(project_id, row, column_mapping)
                tasks.append(task)
            except (KeyError, ValueError, TypeError) as exc:
                errors.append(ImportError(row=i, message=str(exc)))
                logger.warning("Import row %d failed: %s", i, exc)

        # Сохраняем успешные задачи
        if tasks:
            await self._task_repo.bulk_save(tasks)

        # Пишем лог
        status = (
            ImportStatus.SUCCESS
            if not errors
            else (ImportStatus.PARTIAL if tasks else ImportStatus.FAILED)
        )

        log = ImportLog(
            project_id=project_id,
            filename=filename,
            rows_imported=len(tasks),
            rows_failed=len(errors),
            status=status,
            column_mapping=column_mapping,
            error_details=(
                {"errors": [{"row": e.row, "message": e.message} for e in errors]}
                if errors
                else None
            ),
        )
        saved_log = await self._import_log_repo.save(log)

        return ImportResult(
            tasks_created=len(tasks),
            errors=errors,
            log_id=saved_log.id,
        )

    # ---------- Helpers ----------

    @staticmethod
    def _row_to_task(
        project_id: UUID,
        row: dict,
        column_mapping: dict,
    ) -> Task:
        """Преобразовать одну строку Excel в Task."""
        # Обязательное поле — название задачи
        title_col = column_mapping.get("task_title")
        if not title_col:
            raise ValueError("column_mapping must contain 'task_title'")

        title = row.get(title_col)
        if not title or not str(title).strip():
            raise ValueError(f"Empty task title in column '{title_col}'")

        return Task(
            project_id=project_id,
            title=str(title).strip()[:500],
            description=_opt_str(row, column_mapping.get("description")),
            deadline=_opt_date(row, column_mapping.get("deadline")),
            section_code=_opt_str(row, column_mapping.get("section")),
            to_section_code=_opt_str(row, column_mapping.get("to_section")),
            status=TaskStatus.NOT_STARTED,
            source="import",
        )


def _opt_str(row: dict, column: str | None) -> str | None:
    """Безопасно достать строку из строки Excel."""
    if not column:
        return None
    value = row.get(column)
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _opt_date(row: dict, column: str | None) -> date | None:
    """Безопасно достать дату из строки Excel."""
    if not column:
        return None
    value = row.get(column)
    if value is None or value == "":
        return None

    # Уже date/datetime
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value

    # Строка — пробуем распарсить
    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue

    raise ValueError(f"Cannot parse date '{text}' (column '{column}')")