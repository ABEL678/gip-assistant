"""Отдельный Python-воркер для парсинга Excel.

Запускается как самостоятельный процесс (см. docker-compose.yml).
Опрашивает таблицу import_logs со статусом 'parsing' каждые 5 секунд.
"""

import asyncio
import logging

from backend.src.bootstrap import get_container

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("excel_worker")

POLL_INTERVAL = 5  # секунд


async def process_queue() -> None:
    """Основной цикл воркера."""
    container = get_container()
    logger.info(
        "Excel worker started. App=%s, Env=%s",
        container.settings.APP_NAME,
        container.settings.APP_ENV,
    )

    while True:
        try:
            # TODO MVP: импорт из import_logs со статусом 'parsing'
            # log = await container.import_log_repo.get_pending()
            # if log:
            #     await container.import_service.process_import(log.id)
            await asyncio.sleep(POLL_INTERVAL)
        except asyncio.CancelledError:
            logger.info("Worker stopped.")
            break
        except Exception as exc:  # noqa: BLE001
            logger.exception("Worker error: %s", exc)
            await asyncio.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    asyncio.run(process_queue())