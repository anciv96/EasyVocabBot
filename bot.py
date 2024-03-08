import asyncio
import logging
import sys

from src.view.dispatcher import bot, db
from src.view.handlers import dp


async def main() -> None:
    await db.connect()
    await dp.start_polling(bot)
    await db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
