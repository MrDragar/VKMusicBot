import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from src.commands import register_commands
from src.containers import Container
from src.database.init_database import init_db, close_db
from src.handlers import router
from src.middlewares import setup_i18n


async def main() -> None:
    container = Container()
    container.config.load()
    session = AiohttpSession(timeout=0)
    bot = Bot(token=container.config.get("API_TOKEN"), session=session)
    dp = Dispatcher(container=container)
    await init_db()
    setup_i18n(dp)
    dp.include_router(router)
    await register_commands(bot, container)
    await dp.start_polling(bot)
    await close_db()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())
