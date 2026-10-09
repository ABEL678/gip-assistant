"""Тесты Excel-парсера."""

import io

import pytest
from openpyxl import Workbook

from backend.src.adapters.import_export.excel_parser import (
    ExcelParseError,
    parse_excel,
)


def _make_xlsx(rows: list[list]) -> bytes:
    """Собрать .xlsx в памяти из списка строк."""
    wb = Workbook()
    ws = wb.active
    for row in rows:
        ws.append(row)
    buf = io.BytesIO()
    wb.save(buf)
    wb.close()
    return buf.getvalue()


# ---------- Успешный парсинг ----------


def test_parse_simple():
    """Простейший Excel: 2 колонки, 2 строки."""
    data = _make_xlsx(
        [
            ["Наименование", "Срок"],
            ["Задача 1", "2026-10-20"],
            ["Задача 2", "2026-11-01"],
        ]
    )

    result = parse_excel(data)

    assert result.columns == ["Наименование", "Срок"]
    assert len(result.rows) == 2
    assert result.rows[0]["Наименование"] == "Задача 1"
    assert result.rows[0]["Срок"] == "2026-10-20"
    assert result.rows[1]["Наименование"] == "Задача 2"


def test_parse_with_empty_cells():
    """Пустые ячейки → None."""
    data = _make_xlsx(
        [
            ["Наименование", "Описание"],
            ["Задача 1", None],
            ["Задача 2", ""],
        ]
    )

    result = parse_excel(data)

    assert result.rows[0]["Описание"] is None
    assert result.rows[1]["Описание"] is None


def test_parse_with_empty_string_spaces():
    """Строка из пробелов → None."""
    data = _make_xlsx(
        [
            ["Наименование", "Описание"],
            ["Задача 1", "   "],
        ]
    )

    result = parse_excel(data)

    assert result.rows[0]["Описание"] is None


def test_parse_skips_empty_rows():
    """Полностью пустые строки — пропускаются."""
    data = _make_xlsx(
        [
            ["Наименование", "Срок"],
            ["Задача 1", "2026-10-20"],
            [None, None],  # пустая
            ["Задача 2", "2026-11-01"],
            ["", ""],  # пустая
        ]
    )

    result = parse_excel(data)

    assert len(result.rows) == 2
    assert result.rows[0]["Наименование"] == "Задача 1"
    assert result.rows[1]["Наименование"] == "Задача 2"


def test_parse_strips_whitespace():
    """Пробелы в значениях — обрезаются."""
    data = _make_xlsx(
        [
            ["  Наименование  ", "Срок"],
            ["  Задача 1  ", "  2026-10-20  "],
        ]
    )

    result = parse_excel(data)

    assert result.columns == ["Наименование", "Срок"]
    assert result.rows[0]["Наименование"] == "Задача 1"
    assert result.rows[0]["Срок"] == "2026-10-20"


def test_parse_preview_max_rows():
    """max_rows=2 — только первые 2 строки."""
    data = _make_xlsx(
        [
            ["Наименование", "Срок"],
            ["A", "2026-01-01"],
            ["B", "2026-01-02"],
            ["C", "2026-01-03"],
            ["D", "2026-01-04"],
        ]
    )

    result = parse_excel(data, max_rows=2)

    assert len(result.rows) == 2
    assert result.rows[0]["Наименование"] == "A"
    assert result.rows[1]["Наименование"] == "B"


def test_parse_dates_as_date_objects():
    """Даты из Excel приходят как datetime.date."""
    from datetime import date

    data = _make_xlsx(
        [
            ["Наименование", "Срок"],
            ["Задача", date(2026, 10, 20)],
        ]
    )

    result = parse_excel(data)

    assert result.rows[0]["Срок"] == date(2026, 10, 20)


def test_parse_duplicate_columns():
    """Дубли имён колонок — добавляется суффикс."""
    data = _make_xlsx(
        [
            ["Наименование", "Наименование", "Срок"],
            ["A", "B", "2026-10-20"],
        ]
    )

    result = parse_excel(data)

    assert result.columns == ["Наименование", "Наименование_2", "Срок"]


def test_parse_skips_empty_columns():
    """Пустые заголовки — пропускаются."""
    data = _make_xlsx(
        [
            ["Наименование", None, "Срок", ""],
            ["Задача 1", "x", "2026-10-20", "y"],
        ]
    )

    result = parse_excel(data)

    assert result.columns == ["Наименование", "Срок"]
    assert result.rows[0] == {
        "Наименование": "Задача 1",
        "Срок": "2026-10-20",
    }


# ---------- Ошибки ----------


def test_parse_empty_bytes():
    """Пустые байты → ошибка."""
    with pytest.raises(ExcelParseError, match="пуст"):
        parse_excel(b"")


def test_parse_invalid_file():
    """Не Excel → ошибка."""
    with pytest.raises(ExcelParseError, match="Не удалось прочитать"):
        parse_excel(b"not an excel file at all")


def test_parse_header_only():
    """Только заголовки, без строк данных → ошибка (нет смысла импортировать)."""
    data = _make_xlsx([["Наименование", "Срок"]])

    with pytest.raises(ExcelParseError, match="Не удалось найти строку заголовков"):
        parse_excel(data)


# ---------- Новые тесты: автопоиск заголовков, suggested_mapping, preview_rows_raw ----------


def test_parse_header_not_in_first_row():
    """Заголовки на 3-й строке — находятся автоматически."""
    data = _make_xlsx(
        [
            ["Проект X", None, None],
            ["ГИП: Иванов", None, None],
            ["Наименование", "Срок", "Раздел"],
            ["Задача 1", "2026-10-20", "АР"],
            ["Задача 2", "2026-11-01", "КР"],
        ]
    )

    result = parse_excel(data)

    assert result.columns == ["Наименование", "Срок", "Раздел"]
    assert len(result.rows) == 2
    assert result.rows[0]["Наименование"] == "Задача 1"
    assert result.header_row_index == 2


def test_parse_header_row_override():
    """Если header_row указан явно — не ищем, используем его."""
    data = _make_xlsx(
        [
            ["мусор", "мусор"],
            ["A", "B"],
            ["C", "D"],
        ]
    )

    result = parse_excel(data, header_row=1)

    assert result.columns == ["A", "B"]
    assert result.rows == [{"A": "C", "B": "D"}]


def test_parse_suggested_mapping():
    """Автоподсказка маппинга по именам колонок."""
    data = _make_xlsx(
        [
            ["Наименование", "Срок", "Раздел", "Ответственный", "Описание"],
            ["Задача 1", "2026-10-20", "АР", "Иванов", "комментарий"],
        ]
    )

    result = parse_excel(data)

    assert result.suggested_mapping == {
        "task_title": "Наименование",
        "deadline": "Срок",
        "section": "Раздел",
        "assignee": "Ответственный",
        "description": "Описание",
    }


def test_parse_suggested_mapping_partial():
    """Если найдена только часть — возвращаются только найденные поля."""
    data = _make_xlsx(
        [
            ["Задача", "Some Column", "Another"],
            ["A", "x", "y"],
        ]
    )

    result = parse_excel(data)

    assert result.suggested_mapping == {"task_title": "Задача"}


def test_parse_preview_rows_raw_present():
    """preview_rows_raw содержит первые N строк файла."""
    data = _make_xlsx(
        [
            ["Шапка 1"],
            ["Наименование", "Срок"],
            ["Задача 1", "2026-10-20"],
        ]
    )

    result = parse_excel(data)

    assert len(result.preview_rows_raw) >= 3
    # Первая строка файла — "Шапка 1"
    assert "Шапка 1" in result.preview_rows_raw[0]

