"""Запуск Telegram-бота в режиме polling (для локальной разработки).

В продакшене используем webhook (быстрее, дешевле).
"""

import asyncio
import logging

from aiogram import Dispatcher

from backend.src.adapters.notifications.handlers import router
from backend.src.adapters.notifications.telegram_bot import get_bot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("bot_runner")


async def run_polling() -> None:
    """Запустить бота в режиме polling."""
    bot = get_bot()
    dp = Dispatcher()
    dp.include_router(router)

    logger.info("Bot polling started. Press Ctrl+C to stop.")
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(run_polling())
