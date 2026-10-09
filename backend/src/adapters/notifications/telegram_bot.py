"""Telegram-бот на aiogram 3.x.

Реализация ТЗ 3.0, раздел 5.3.
"""

import logging

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from backend.src.config import settings

logger = logging.getLogger(__name__)

_bot: Bot | None = None


def get_bot() -> Bot:
    """Получить singleton-бота.

    Raises:
        RuntimeError: если токен не задан в .env
    """
    global _bot
    if _bot is None:
        if not settings.TELEGRAM_BOT_TOKEN:
            raise RuntimeError(
                "TELEGRAM_BOT_TOKEN не задан в .env. "
                "Получите токен у @BotFather и добавьте в .env"
            )
        _bot = Bot(
            token=settings.TELEGRAM_BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
    return _bot


async def send_message(
    chat_id: int,
    text: str,
    parse_mode: ParseMode = ParseMode.HTML,
) -> bool:
    """Отправить сообщение в чат.

    Returns:
        True — успешно, False — ошибка.
    """
    try:
        bot = get_bot()
        await bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)
        logger.info("Telegram message sent to chat_id=%s", chat_id)
        return True
    except Exception as exc:
        logger.exception("Failed to send Telegram message to %s: %s", chat_id, exc)
        return False