"""Тесты ImportService."""

import pytest

from backend.src.domain.services.import_service import ImportService


@pytest.mark.asyncio
async def test_import_creates_tasks(
    task_repo, import_log_repo, project_id, sample_rows, column_mapping
):
    """Импорт 3 строк → 3 задачи созданы."""
    service = ImportService(task_repo, import_log_repo)

    result = await service.import_excel(
        project_id=project_id,
        rows=sample_rows,
        column_mapping=column_mapping,
        filename="test.xlsx",
    )

    assert result.tasks_created == 3
    assert result.errors == []
    assert task_repo.bulk_save.called


@pytest.mark.asyncio
async def test_import_saves_log(
    task_repo, import_log_repo, project_id, sample_rows, column_mapping
):
    """Импорт создаёт запись в ImportLog."""
    service = ImportService(task_repo, import_log_repo)

    result = await service.import_excel(
        project_id=project_id,
        rows=sample_rows,
        column_mapping=column_mapping,
    )

    assert import_log_repo.save.called
    assert result.log_id is not None


@pytest.mark.asyncio
async def test_import_empty_title_fails(task_repo, import_log_repo, project_id, column_mapping):
    """Строка с пустым title → ошибка."""
    rows = [{"Наименование": "", "Раздел": "ОВ"}]
    service = ImportService(task_repo, import_log_repo)

    result = await service.import_excel(
        project_id=project_id,
        rows=rows,
        column_mapping=column_mapping,
    )

    assert result.tasks_created == 0
    assert len(result.errors) == 1
    assert "Empty task title" in result.errors[0].message


@pytest.mark.asyncio
async def test_import_partial_failures(task_repo, import_log_repo, project_id, column_mapping):
    """2 успешных + 1 пустой = PARTIAL."""
    rows = [
        {"Наименование": "ОК-1", "Раздел": "ОВ"},
        {"Наименование": "", "Раздел": "ОВ"},  # ошибка
        {"Наименование": "ОК-2", "Раздел": "АР"},
    ]
    service = ImportService(task_repo, import_log_repo)

    result = await service.import_excel(
        project_id=project_id,
        rows=rows,
        column_mapping=column_mapping,
    )

    assert result.tasks_created == 2
    assert len(result.errors) == 1
    assert result.errors[0].row == 1


@pytest.mark.asyncio
async def test_import_empty_rows(task_repo, import_log_repo, project_id, column_mapping):
    """Пустой список строк — 0 задач, 0 ошибок."""
    service = ImportService(task_repo, import_log_repo)

    result = await service.import_excel(
        project_id=project_id,
        rows=[],
        column_mapping=column_mapping,
    )

    assert result.tasks_created == 0
    assert result.errors == []


@pytest.mark.asyncio
async def test_import_without_title_mapping(task_repo, import_log_repo, project_id, sample_rows):
    """Если нет 'task_title' в маппинге — ошибки."""
    service = ImportService(task_repo, import_log_repo)

    result = await service.import_excel(
        project_id=project_id,
        rows=sample_rows,
        column_mapping={"section": "Раздел"},  # нет task_title
    )

    assert result.tasks_created == 0
    assert len(result.errors) == len(sample_rows)


@pytest.mark.asyncio
async def test_import_parses_dates(task_repo, import_log_repo, project_id, column_mapping):
    """Разные форматы дат парсятся."""
    rows = [
        {"Наименование": "A", "Срок": "2026-10-20", "Раздел": "ОВ"},
        {"Наименование": "B", "Срок": "15.11.2026", "Раздел": "АР"},
    ]
    service = ImportService(task_repo, import_log_repo)

    result = await service.import_excel(
        project_id=project_id,
        rows=rows,
        column_mapping=column_mapping,
    )

    assert result.tasks_created == 2
