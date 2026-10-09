"""Cron-воркер для отправки ежедневной сводки в 09:00.

Запускается как отдельный процесс (см. docker-compose.yml).
Использует APScheduler или простой loop с проверкой времени.
"""

import asyncio
import logging
from datetime import datetime, time
from zoneinfo import ZoneInfo

from backend.src.adapters.notifications.digest import send_daily_digest

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("digest_worker")

# Moscow time
TZ = ZoneInfo("Europe/Moscow")
DIGEST_TIME = time(hour=9, minute=0)
CHECK_INTERVAL = 60  # проверка раз в минуту


async def run_digest_loop() -> None:
    """Основной цикл: в 09:00 МСК — отправить сводку."""
    logger.info("Digest worker started. Target time: 09:00 MSK")

    last_sent_date = None

    while True:
        try:
            now = datetime.now(TZ)
            today = now.date()

            # Отправляем, если сейчас 09:00-09:01 и не отправляли сегодня
            if (
                now.hour == DIGEST_TIME.hour
                and now.minute == DIGEST_TIME.minute
                and last_sent_date != today
            ):
                logger.info("Sending daily digest...")
                sent = await send_daily_digest()
                logger.info("Digest sent to %d users", sent)
                last_sent_date = today

            await asyncio.sleep(CHECK_INTERVAL)
        except asyncio.CancelledError:
            logger.info("Digest worker stopped.")
            break
        except Exception as exc:
            logger.exception("Digest worker error: %s", exc)
            await asyncio.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    asyncio.run(run_digest_loop())