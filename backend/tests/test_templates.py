"""Тесты шаблонов Telegram."""

from datetime import date
from uuid import uuid4

from backend.src.adapters.notifications.templates import (
    format_digest,
    format_help,
    format_start_message,
)
from backend.src.domain.entities.task import Task


def test_digest_empty():
    """Пустая сводка — сообщение об отсутствии просрочек."""
    text = format_digest(overdue=[], upcoming=[], today=date(2026, 10, 9))
    assert "Просрочек нет" in text


def test_digest_with_overdue():
    """Сводка с просрочкой."""
    project_id = uuid4()
    task = Task(
        project_id=project_id,
        title="Разработка ОВ",
        deadline=date(2026, 10, 1),  # 8 дней назад от 09.10.2026
    )
    text = format_digest(overdue=[task], upcoming=[], today=date(2026, 10, 9))
    assert "Просрочено (1)" in text
    assert "Разработка ОВ" in text
    assert "01.10.2026" in text
    assert "8 дн." in text


def test_digest_with_upcoming():
    """Сводка с близким дедлайном."""
    project_id = uuid4()
    task = Task(
        project_id=project_id,
        title="Проверка АР",
        deadline=date(2026, 10, 11),  # через 2 дня от 09.10.2026
    )
    text = format_digest(overdue=[], upcoming=[task], today=date(2026, 10, 9))
    assert "Скоро дедлайн (1)" in text
    assert "Проверка АР" in text
    assert "через 2 дн." in text


def test_digest_today_deadline():
    """Дедлайн сегодня."""
    project_id = uuid4()
    task = Task(
        project_id=project_id,
        title="Сдача",
        deadline=date(2026, 10, 9),
    )
    text = format_digest(overdue=[], upcoming=[task], today=date(2026, 10, 9))
    assert "сегодня" in text


def test_start_message():
    """Приветствие."""
    text = format_start_message("Иван")
    assert "Привет, Иван" in text
    assert "/link" in text


def test_help():
    """Справка."""
    text = format_help()
    assert "/start" in text
    assert "/link" in text
    assert "/status" in text