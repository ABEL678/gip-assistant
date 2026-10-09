"""Telegram-уведомления."""

from backend.src.adapters.notifications.telegram_bot import (
    get_bot,
    send_message,
)

__all__ = ["get_bot", "send_message"]
