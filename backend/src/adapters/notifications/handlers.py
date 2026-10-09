"""Обработчики команд Telegram-бота."""

import logging

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from backend.src.adapters.db.repositories import (
    SqlAlchemyTaskRepository,
    SqlAlchemyUserRepository,
)
from backend.src.adapters.db.session import AsyncSessionLocal
from backend.src.adapters.notifications.templates import (
    format_digest,
    format_help,
    format_start_message,
)

logger = logging.getLogger(__name__)

router = Router(name="gip_assistant")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Команда /start."""
    name = message.from_user.first_name if message.from_user else None
    await message.answer(format_start_message(name))


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Команда /help."""
    await message.answer(format_help())


@router.message(Command("link"))
async def cmd_link(message: Message) -> None:
    """Команда /link <email> — привязать Telegram к аккаунту."""
    if message.from_user is None:
        return

    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Использование: <code>/link your@email.ru</code>")
        return

    email = parts[1].strip().lower()

    async with AsyncSessionLocal() as session:
        user_repo = SqlAlchemyUserRepository(session)

        user = await user_repo.get_by_email(email)
        if user is None:
            await message.answer(f"Пользователь <b>{email}</b> не найден в ГИП-Ассистент.")
            return

        user.telegram_id = message.from_user.id
        await user_repo.save(user)
        await session.commit()

    await message.answer(
        f"✅ Аккаунт привязан: <b>{email}</b>\n\n"
        "Теперь буду присылать сводку каждый день в 09:00."
    )
    logger.info("User %s linked to telegram_id=%s", email, message.from_user.id)


@router.message(Command("status"))
async def cmd_status(message: Message) -> None:
    """Команда /status — текущие просрочки и дедлайны."""
    async with AsyncSessionLocal() as session:
        task_repo = SqlAlchemyTaskRepository(session)
        overdue = await task_repo.get_overdue()
        upcoming = await task_repo.get_upcoming(days=3)

    text = format_digest(overdue=overdue, upcoming=upcoming)
    await message.answer(text)


@router.message()
async def cmd_fallback(message: Message) -> None:
    """Ответ на неизвестные сообщения."""
    await message.answer("Не знаю такой команды. Напиши /help для списка команд.")
