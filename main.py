from aiogram import Bot, Dispatcher

import asyncio
import logging
import sys

from bot.database.init_database import init_db, close_db
from bot.middlewares import setup_i18n
from bot.handlers import root_router
from bot.commands import register_commands
from bot.containers import Container


async def main() -> None:
    container = Container()
    container.config.load()
    bot = Bot(token=container.config.get("API_TOKEN"))
    dp = Dispatcher(container=container)
    await init_db()
    setup_i18n(dp)
    dp.include_router(root_router)
    await register_commands(bot)
    await dp.start_polling(bot)
    await close_db()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
