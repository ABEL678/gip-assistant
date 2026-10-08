"""Парсер Excel-файлов.

Читает байты .xlsx через openpyxl и возвращает список строк (list[dict]).
Не знает о домене — просто "сырые" строки + заголовки.

Пример использования:

    from backend.src.adapters.import_export import parse_excel

    with open("tasks.xlsx", "rb") as f:
        result = parse_excel(f.read())

    print(result.columns)      # ['Наименование', 'Срок', ...]
    print(result.rows[0])      # {'Наименование': 'Разработка ОВ', ...}
"""

import io
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from zipfile import BadZipFile

from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

logger = logging.getLogger(__name__)

# Максимальный размер файла (10 MB, см. ТЗ 3.0, раздел 9)
MAX_FILE_SIZE = 10 * 1024 * 1024


class ExcelParseError(Exception):
    """Ошибка парсинга Excel."""


@dataclass
class ExcelParseResult:
    """Результат парсинга Excel."""

    columns: list[str] = field(default_factory=list)
    rows: list[dict[str, Any]] = field(default_factory=list)
    total_rows: int = 0


def parse_excel(
    file_bytes: bytes,
    max_rows: int | None = None,
) -> ExcelParseResult:
    """Разобрать Excel-файл в список строк.

    Args:
        file_bytes: Содержимое .xlsx файла (байты).
        max_rows: Если указано — вернуть только первые N строк
            (для preview-режима). None = все строки.

    Returns:
        ExcelParseResult с колонками и строками.

    Raises:
        ExcelParseError: если файл пуст, повреждён или больше 10 MB.
    """
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
            read_only=True,
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
        # 3. Взять первый лист
        ws = wb.active
        if ws is None:
            raise ExcelParseError("В файле нет активного листа")

        rows_iter = ws.iter_rows(values_only=True)

        # 4. Первая строка = заголовки
        try:
            header_row = next(rows_iter)
        except StopIteration as exc:
            raise ExcelParseError("Файл пуст (нет строк)") from exc

        # columns_with_indices — список (index_in_row, column_name)
        # Это важно: если пропускаем пустые заголовки,
        # значения всё равно берём из ПРАВИЛЬНОЙ позиции.
        columns_with_indices = _extract_columns_with_indices(header_row)
        if not columns_with_indices:
            raise ExcelParseError("Не найдены колонки в первой строке")

        columns = [name for _, name in columns_with_indices]

        # 5. Парсим строки
        rows: list[dict[str, Any]] = []
        for row_idx, raw_row in enumerate(rows_iter, start=2):
            # Пропускаем полностью пустые строки
            if _is_empty_row(raw_row):
                continue

            row_dict = _row_to_dict(columns_with_indices, raw_row)
            rows.append(row_dict)

            if max_rows is not None and len(rows) >= max_rows:
                break

        total_rows = len(rows)

        logger.info(
            "Parsed Excel: %d columns, %d rows%s",
            len(columns),
            total_rows,
            f" (preview, max={max_rows})" if max_rows else "",
        )

        return ExcelParseResult(
            columns=columns,
            rows=rows,
            total_rows=total_rows,
        )
    finally:
        wb.close()


# ---------- Helpers ----------


def _extract_columns_with_indices(
    header_row: tuple,
) -> list[tuple[int, str]]:
    """Извлечь (индекс_в_строке, имя_колонки), пропуская пустые заголовки.

    Возвращает список кортежей, где первый элемент — позиция колонки
    в исходной строке Excel, второй — нормализованное имя.
    """
    result: list[tuple[int, str]] = []
    seen: set[str] = set()

    for idx, cell in enumerate(header_row):
        if cell is None:
            continue
        name = str(cell).strip()
        if not name:
            continue

        # Уникальные имена (если дубли — суффикс _2, _3, ...)
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
    """Преобразовать строку Excel в dict.

    Значения берутся из правильных позиций (по индексам из header).
    """
    row_dict: dict[str, Any] = {}
    for idx, col_name in columns_with_indices:
        value = raw_row[idx] if idx < len(raw_row) else None
        row_dict[col_name] = _normalize_value(value)
    return row_dict


def _normalize_value(value: Any) -> Any:
    """Нормализовать значение из ячейки Excel.

    - Пустые строки → None
    - Строки с пробелами → strip
    - datetime → date (Excel не различает)
    - Остальное (числа) → как есть
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        text = value.strip()
        return text if text else None
    return value


def _is_empty_row(raw_row: tuple) -> bool:
    """Проверить, что строка полностью пустая."""
    for cell in raw_row:
        if cell is not None and str(cell).strip():
            return False
    return True
