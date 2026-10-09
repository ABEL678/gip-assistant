"""Универсальный парсер Excel-файлов.

Читает байты .xlsx через openpyxl и возвращает список строк (list[dict]).
Не знает о домене — просто "сырые" строки + заголовки + подсказка маппинга.

Универсальность:
  - Автопоиск строки заголовков (не обязательно первая)
  - Возможность указать строку заголовков вручную (header_row)
  - Разворачивание merged cells
  - Нормализация имён колонок (trim, дубли → _2)
  - Excel-serial даты → datetime.date
  - Автоподсказка маппинга (suggested_mapping)
  - Возврат первых N сырых строк для UI-селектора заголовков
"""

import io
import logging
import re
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Any
from zipfile import BadZipFile

from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

logger = logging.getLogger(__name__)

# Максимальный размер файла (10 MB, см. ТЗ 3.0, раздел 9)
MAX_FILE_SIZE = 10 * 1024 * 1024

# Сколько первых строк сканируем в поисках заголовков
HEADER_SEARCH_DEPTH = 10

# Сколько сырых строк отдавать в UI для ручного выбора заголовка
PREVIEW_RAW_DEPTH = 10

# Excel serial date epoch (1900-01-01, с поправкой на "високосный" 1900)
_EXCEL_EPOCH = datetime(1899, 12, 30)


class ExcelParseError(Exception):
    """Ошибка парсинга Excel."""


@dataclass
class ExcelParseResult:
    """Результат парсинга Excel."""

    columns: list[str] = field(default_factory=list)
    rows: list[dict[str, Any]] = field(default_factory=list)
    total_rows: int = 0
    suggested_mapping: dict[str, str] = field(default_factory=dict)
    header_row_index: int = 0  # 0-based индекс строки заголовков
    preview_rows_raw: list[list] = field(default_factory=list)  # первые N строк для UI
    sheet_name: str = ""  # имя активного листа


# ---------- Алиасы для автоподсказки маппинга ----------

_MAPPING_ALIASES: dict[str, list[str]] = {
    "task_title": [
        "название", "наименование", "задача", "работа", "титул",
        "задание", "тип",  # для реестров заданий
        "title", "name", "task", "subject",
    ],
    "deadline": [
        "срок", "дедлайн", "дата окончания", "дата завершения",
        "окончание", "дата выдачи", "дата", "сроки",
        "deadline", "due date", "due", "end date", "date",
    ],
    "section": [
        "раздел", "секция", "марка", "дисциплина", "специальность",
        "кому",  # в реестрах заданий "кому" — это раздел-получатель
        "section", "discipline", "trade",
    ],
    "assignee": [
        "исполнитель", "ответственный", "assignee", "owner",
        "responsible", "выполнил", "от кого",
    ],
    "description": [
        "описание", "комментарий", "примечание", "заметка",
        "description", "comment", "note", "details",
    ],
}


def parse_excel(
    file_bytes: bytes,
    max_rows: int | None = None,
    header_row: int | None = None,
) -> ExcelParseResult:
    """..."""
    # 1. Проверка размера
    if not file_bytes:
        raise ExcelParseError("Файл пуст")

    if len(file_bytes) > MAX_FILE_SIZE:
        raise ExcelParseError(
            f"Файл слишком большой: {len(file_bytes)} байт. "
            f"Максимум: {MAX_FILE_SIZE} байт (10 MB)"
        )

    # 2. Открыть workbook
    try:
        wb = load_workbook(
            io.BytesIO(file_bytes),
            read_only=False,
            data_only=True,
        )
    except (
        InvalidFileException,
        BadZipFile,
        OSError,
        KeyError,
        ValueError,
    ) as exc:
        raise ExcelParseError(f"Не удалось прочитать файл: {exc}") from exc

    try:
        ws = wb.active
        if ws is None:
            raise ExcelParseError("В файле нет активного листа")

        sheet_name = ws.title or ""

        # 3. Построить карту merged cells (НЕ разворачиваем сам лист)
        merged_map = _build_merged_map(ws)

        # 4. Считать все строки с учётом merged_map
        all_rows = _read_all_rows(ws, merged_map)
        if not all_rows:
            raise ExcelParseError("Файл пуст (нет строк)")

        # 5. Определить строку заголовков
        if header_row is not None:
            if header_row < 0 or header_row >= len(all_rows):
                raise ExcelParseError(
                    f"Указанная строка заголовков #{header_row} вне диапазона "
                    f"(всего строк: {len(all_rows)})"
                )
            header_idx = header_row
        else:
            header_idx = _detect_header_row(all_rows[:HEADER_SEARCH_DEPTH])
            if header_idx is None:
                raise ExcelParseError(
                    f"Не удалось найти строку заголовков "
                    f"в первых {HEADER_SEARCH_DEPTH} строках. "
                    f"Укажите header_row вручную."
                )

        header_values = all_rows[header_idx]

        # 6. Извлечь колонки
        columns_with_indices = _extract_columns_with_indices(header_values)
        if not columns_with_indices:
            raise ExcelParseError(
                f"Не найдены колонки в строке заголовков #{header_idx}"
            )

        columns = [name for _, name in columns_with_indices]

        # 7. Парсим строки данных
        rows: list[dict[str, Any]] = []
        for raw_row in all_rows[header_idx + 1:]:
            if _is_empty_row(raw_row):
                continue
            if _is_numbering_row(raw_row):
                continue
            row_dict = _row_to_dict(columns_with_indices, raw_row)
            if all(v is None for v in row_dict.values()):
                continue
            rows.append(row_dict)
            if max_rows is not None and len(rows) >= max_rows:
                break

        total_rows = len(rows)

        # 8. Автоподсказка маппинга
        suggested = _suggest_mapping(columns)

        # 9. Первые N сырых строк для UI-селектора
        preview_rows_raw = [
            [_to_json_value(cell) for cell in row]
            for row in all_rows[:PREVIEW_RAW_DEPTH]
        ]

        logger.info(
            "Parsed Excel '%s': header_row=%d, %d columns, %d rows, "
            "suggested_mapping=%s",
            sheet_name,
            header_idx,
            len(columns),
            total_rows,
            suggested,
        )

        return ExcelParseResult(
            columns=columns,
            rows=rows,
            total_rows=total_rows,
            suggested_mapping=suggested,
            header_row_index=header_idx,
            preview_rows_raw=preview_rows_raw,
            sheet_name=sheet_name,
        )
    finally:
        wb.close()


def _read_all_rows(ws, merged_map: dict[tuple[int, int], Any]) -> list[tuple]:
    """Прочитать все строки листа в виде list[tuple] с учётом merged_map.

    Для каждой ячейки:
      - если (row, col) в merged_map → берём значение оттуда
      - иначе → читаем как обычно
    """
    rows: list[tuple] = []
    for row_idx, row in enumerate(ws.iter_rows(values_only=False), start=1):
        values: list[Any] = []
        for col_idx, cell in enumerate(row, start=1):
            key = (row_idx, col_idx)
            if key in merged_map:
                values.append(merged_map[key])
            else:
                # MergedCell (кроме верхней левой) — value не читается нормально,
                # но у нас для них всегда есть запись в merged_map.
                # Если её нет — значит это обычная пустая ячейка.
                if type(cell).__name__ == "MergedCell":
                    values.append(None)
                else:
                    values.append(cell.value)
        rows.append(tuple(values))
    return rows


# ---------- Merged cells ----------


def _build_merged_map(ws) -> dict[tuple[int, int], Any]:
    """Построить карту: (row, col) -> значение из верхней левой ячейки merged range.

    openpyxl не даёт читать/писать MergedCell напрямую, поэтому
    мы строим карту и подставляем значения вручную при парсинге строк.
    """
    merged_map: dict[tuple[int, int], Any] = {}
    if not ws.merged_cells.ranges:
        return merged_map

    for merged_range in ws.merged_cells.ranges:
        top_left = ws.cell(
            row=merged_range.min_row,
            column=merged_range.min_col,
        )
        value = top_left.value
        if value is None:
            continue
        for row in range(merged_range.min_row, merged_range.max_row + 1):
            for col in range(merged_range.min_col, merged_range.max_col + 1):
                merged_map[(row, col)] = value

    return merged_map


# ---------- Поиск строки заголовков ----------


def _detect_header_row(rows: list[tuple]) -> int | None:
    """Найти индекс строки заголовков среди первых N строк.

    Эвристика:
      +1 за каждую непустую ячейку
      +3 если ячейка похожа на имя поля (по алиасам)
      -2 если ячейка — дата/число
      -5 если >50% ячеек пусты
      -100 если под строкой нет ни одной непустой строки
      -3 если ни одного алиаса в строке
    """
    if not rows:
        return None

    best_idx: int | None = None
    best_score = -10**9

    for idx, row in enumerate(rows):
        has_data_below = any(
            not _is_empty_row(r) for r in rows[idx + 1:]
        )
        if not has_data_below:
            continue

        score = _score_header_row(row)
        if score > best_score:
            best_score = score
            best_idx = idx

    return best_idx


def _score_header_row(row: tuple) -> int:
    """Оценить, насколько строка похожа на заголовки."""
    if not row:
        return -1000

    total = len(row)
    non_empty = 0
    alias_hits = 0
    date_or_number = 0

    for cell in row:
        if cell is None or (isinstance(cell, str) and not cell.strip()):
            continue
        non_empty += 1
        if isinstance(cell, (int, float, datetime, date)):
            date_or_number += 1
            continue
        if isinstance(cell, str):
            if _matches_any_alias(cell):
                alias_hits += 1

    if non_empty == 0:
        return -1000

    score = non_empty
    score += alias_hits * 3
    score -= date_or_number * 2

    if non_empty < total / 2:
        score -= 5

    if alias_hits == 0:
        score -= 3

    return score


def _matches_any_alias(text: str) -> bool:
    """Проверить, встречается ли текст в списке алиасов."""
    normalized = _normalize_for_match(text)
    if not normalized:
        return False
    for aliases in _MAPPING_ALIASES.values():
        for alias in aliases:
            if alias in normalized:
                return True
    return False


def _normalize_for_match(text: str) -> str:
    """Нормализовать текст: lower, strip, ё→е, без лишних пробелов."""
    if not text:
        return ""
    text = str(text).lower().strip()
    text = text.replace("ё", "е")
    text = re.sub(r"\s+", " ", text)
    return text


# ---------- Маппинг ----------


def _suggest_mapping(columns: list[str]) -> dict[str, str]:
    """Подобрать автоматический маппинг по именам колонок."""
    result: dict[str, str] = {}
    used_columns: set[str] = set()

    field_priority = ["task_title", "deadline", "section", "assignee", "description"]

    for field_name in field_priority:
        aliases = _MAPPING_ALIASES[field_name]
        best_match: str | None = None
        best_score = 0

        for column in columns:
            if column in used_columns:
                continue
            normalized = _normalize_for_match(column)
            for alias in aliases:
                if normalized == alias:
                    score = 100 + len(alias)
                elif normalized.startswith(alias):
                    score = 50 + len(alias)
                elif alias in normalized:
                    score = 20 + len(alias)
                else:
                    continue

                if score > best_score:
                    best_score = score
                    best_match = column

        if best_match:
            result[field_name] = best_match
            used_columns.add(best_match)

    return result


# ---------- Колонки и строки ----------


def _extract_columns_with_indices(
    header_row: tuple,
) -> list[tuple[int, str]]:
    """Извлечь (индекс_в_строке, имя_колонки), пропуская пустые заголовки."""
    result: list[tuple[int, str]] = []
    seen: set[str] = set()

    for idx, cell in enumerate(header_row):
        if cell is None:
            continue
        name = str(cell).strip()
        if not name:
            continue

        base_name = name
        counter = 2
        while name in seen:
            name = f"{base_name}_{counter}"
            counter += 1

        seen.add(name)
        result.append((idx, name))

    return result


def _row_to_dict(
    columns_with_indices: list[tuple[int, str]],
    raw_row: tuple,
) -> dict[str, Any]:
    """Преобразовать строку Excel в dict."""
    row_dict: dict[str, Any] = {}
    for idx, col_name in columns_with_indices:
        value = raw_row[idx] if idx < len(raw_row) else None
        row_dict[col_name] = _normalize_value(value)
    return row_dict


def _normalize_value(value: Any) -> Any:
    """Нормализовать значение из ячейки Excel.

    - Пустые строки → None
    - Строки → strip
    - datetime → date
    - Excel-serial числа (36526..73050) → date
    - Остальное — как есть
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        text = value.strip()
        return text if text else None
    if isinstance(value, (int, float)) and 36526 <= value <= 73050:
        if isinstance(value, float) and not value.is_integer():
            return value
        try:
            return (_EXCEL_EPOCH + timedelta(days=int(value))).date()
        except (OverflowError, ValueError):
            return value
    return value


def _is_empty_row(raw_row: tuple) -> bool:
    """Проверить, что строка полностью пустая."""
    for cell in raw_row:
        if cell is not None and str(cell).strip():
            return False
    return True


def _is_numbering_row(raw_row: tuple) -> bool:
    """Похожа ли строка на нумерацию колонок (1, 2, 3, ..., N).

    Признаки:
      - все непустые ячейки — целые числа
      - идут почти подряд (начиная с 1)
      - минимум 3 числа
    """
    numbers: list[int] = []
    for cell in raw_row:
        if cell is None:
            continue
        if isinstance(cell, bool):
            return False
        if isinstance(cell, int):
            numbers.append(cell)
        elif isinstance(cell, float) and cell.is_integer():
            numbers.append(int(cell))
        elif isinstance(cell, str) and cell.strip().isdigit():
            numbers.append(int(cell.strip()))
        else:
            return False  # не число → строка не про нумерацию

    if len(numbers) < 3:
        return False

    # Идём по порядку, допускаем пропуски (1, 2, 4, 5 — тоже нумерация)
    expected = 1
    for n in numbers:
        if n < expected:
            return False
        expected = n + 1

    return True


def _to_json_value(value: Any) -> Any:
    """Преобразовать значение ячейки в JSON-сериализуемое (для preview_rows_raw)."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, (int, float, str, bool)):
        return value
    return str(value)