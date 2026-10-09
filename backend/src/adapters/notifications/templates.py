"""Шаблоны сообщений Telegram.

Формат из ТЗ 3.0, раздел 5.3.2.
"""

from datetime import date

from backend.src.domain.entities.task import Task


def format_digest(
    overdue: list[Task],
    upcoming: list[Task],
    today: date | None = None,
) -> str:
    """Сформировать утреннюю сводку.

    Args:
        overdue: Просроченные задачи.
        upcoming: Задачи с близким дедлайном (3 дня).
        today: Сегодняшняя дата (для тестов).

    Returns:
        Отформатированный текст (HTML).
    """
    today = today or date.today()
    parts: list[str] = ["<b>Утренняя сводка ГИП-Ассистент</b>\n"]

    if overdue:
        parts.append(f"<b>Просрочено ({len(overdue)}):</b>")
        for task in overdue:
            days_late = (today - task.deadline).days if task.deadline else 0
            deadline_str = task.deadline.strftime("%d.%m.%Y") if task.deadline else "—"
            parts.append(
                f"  • {task.title} (срок: {deadline_str}, "
                f"просрочка: {days_late} дн.)"
            )
        parts.append("")

    if upcoming:
        parts.append(f"<b>Скоро дедлайн ({len(upcoming)}):</b>")
        for task in upcoming:
            days_left = (task.deadline - today).days if task.deadline else 0
            deadline_str = task.deadline.strftime("%d.%m.%Y") if task.deadline else "—"
            if days_left == 0:
                days_str = "сегодня"
            elif days_left == 1:
                days_str = "завтра"
            else:
                days_str = f"через {days_left} дн."
            parts.append(f"  • {task.title} (срок: {deadline_str}, {days_str})")
        parts.append("")

    if not overdue and not upcoming:
        parts.append("Просрочек нет. Дедлайнов в ближайшие 3 дня нет. ✅")

    return "\n".join(parts).strip()


def format_start_message(name: str | None = None) -> str:
    """Приветственное сообщение для /start."""
    greeting = f"Привет, {name}!" if name else "Привет!"
    return (
        f"{greeting}\n\n"
        "<b>ГИП-Ассистент</b> — уведомления о просрочках и дедлайнах.\n\n"
        "<b>Команды:</b>\n"
        "  /link &lt;email&gt; — привязать аккаунт\n"
        "  /status — текущие задачи\n"
        "  /help — помощь\n\n"
        "После привязки буду присылать сводку каждый день в 09:00."
    )


def format_help() -> str:
    """Справка /help."""
    return (
        "<b>ГИП-Ассистент — справка</b>\n\n"
        "/start — приветствие\n"
        "/link &lt;email&gt; — привязать Telegram к аккаунту\n"
        "/status — показать текущие просрочки\n"
        "/help — эта справка"
    )