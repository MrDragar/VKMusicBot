from datetime import date

from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.handlers import MessageHandler

from src.database.day_statistic import get_monthly_statistics, get_day_statistic

router = Router()


@router.message(Command("get_month_statistic"))
class SentMonthlyStatisticHandler(MessageHandler):
    async def handle(self):
        result = await get_monthly_statistics(date.today())
        await self.bot.send_message(
            chat_id=self.chat.id,
            text="За этот месяц новых пользователей: {0} \n"
                 "Скачиваний: {1} \n"
                 "Каких-то ошибок: {2}"
            .format(result["new_users"],
                    result["downloads"],
                    result["errors"])
        )


@router.message(Command("get_day_statistic"))
class SentMonthlyStatisticHandler(MessageHandler):
    async def handle(self):
        result = await get_day_statistic()
        await self.bot.send_message(
            chat_id=self.chat.id,
            text="За этот день новых пользователей: {0} \n"
                 "Успешных запросов: {1} \n"
                 "Запросов с неотловленной ошибкой: {2}"
            .format(result.new_users,
                    result.downloads,
                    result.errors)
        )
