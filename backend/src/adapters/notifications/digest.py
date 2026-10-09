"""Отправка ежедневной сводки.

Реализация ТЗ 3.0, раздел 5.3.
"""

import logging

from backend.src.adapters.db.repositories import (
    SqlAlchemyTaskRepository,
    SqlAlchemyUserRepository,
)
from backend.src.adapters.db.session import AsyncSessionLocal
from backend.src.adapters.notifications.telegram_bot import send_message
from backend.src.adapters.notifications.templates import format_digest

logger = logging.getLogger(__name__)


async def send_daily_digest() -> int:
    """Отправить сводку всем привязанным пользователям.

    Returns:
        Количество отправленных сообщений.
    """
    sent = 0

    async with AsyncSessionLocal() as session:
        task_repo = SqlAlchemyTaskRepository(session)
        user_repo = SqlAlchemyUserRepository(session)

        # Получить все задачи
        overdue = await task_repo.get_overdue()
        upcoming = await task_repo.get_upcoming(days=3)

        # Получить всех активных пользователей с Telegram
        users = await user_repo.get_all_with_telegram()

        logger.info(
            "Digest: %d overdue, %d upcoming, %d users",
            len(overdue),
            len(upcoming),
            len(users),
        )

        for user in users:
            # По MVP — отправляем всем одну и ту же сводку
            # (в MVP-2 будет фильтрация по проекту/исполнителю)
            text = format_digest(overdue=overdue, upcoming=upcoming)
            ok = await send_message(chat_id=user.telegram_id, text=text)
            if ok:
                sent += 1

    return sent
