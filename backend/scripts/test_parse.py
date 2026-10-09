"""Быстрая проверка парсера на реальном файле.

Запуск:
    python -m backend.scripts.test_parse "01_Реестр заданий ИОС_НЧ.xlsx"
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.src.adapters.import_export.excel_parser import parse_excel


def main() -> None:
    if len(sys.argv) < 2:
        print("Использование: python -m backend.scripts.test_parse <path-to-xlsx>")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Файл не найден: {filepath}")
        sys.exit(1)

    data = filepath.read_bytes()

    print("=" * 70)
    print(f"Файл: {filepath.name}, {len(data)} байт")
    print("=" * 70)

    result = parse_excel(data, max_rows=5)

    print(f"\n>>> sheet_name = {result.sheet_name!r}")
    print(f">>> header_row_index = {result.header_row_index}")
    print(f">>> total_rows = {result.total_rows}")
    print(f">>> columns ({len(result.columns)}):")
    for c in result.columns:
        print(f"    - {c!r}")

    print("\n>>> suggested_mapping:")
    for field, col in result.suggested_mapping.items():
        print(f"    {field} -> {col!r}")

    print("\n>>> первые 3 строки данных:")
    for i, row in enumerate(result.rows[:3]):
        print(f"\n  Строка {i}:")
        for k, v in row.items():
            print(f"    {k!r}: {v!r}")

    print("\n>>> preview_rows_raw (первые 3 строки файла):")
    for i, row in enumerate(result.preview_rows_raw[:3]):
        print(f"  [{i}]: {row}")

    print("\n>>> preview_rows_raw (строки 5-9 файла):")
    for i, row in enumerate(result.preview_rows_raw[5:10], start=5):
        print(f"  [{i}]: {row}")


if __name__ == "__main__":
    main()