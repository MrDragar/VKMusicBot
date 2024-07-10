import logging

from aiogram import Router
from aiogram.utils.i18n import gettext as _

from src.database.day_statistic import add_error
from src.handlers.base_handlers import StateErrorHandler

router = Router()


@router.errors()
class YoutubeErrorHandler(StateErrorHandler):
    async def handle(self):
        logging.error(self.event.exception)
        await self.state.clear()

        await self.bot.send_message(
            self.event.update.message.chat.id,
            self.event.update.message.text
        )

        await self.bot.send_message(
            self.event.update.message.chat.id,
            _("Произошла какая-то ошибка. Если не сложно, скиньте админам "
              "её текст и описание ваших действий (/send_feedback)")
        )

        await add_error()
