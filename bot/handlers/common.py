from typing import Any, Union

from aiogram.dispatcher.router import Router
from aiogram.handlers import CallbackQueryHandler
from aiogram.filters import Command
from aiogram import types, Bot
from aiogram.utils.i18n import lazy_gettext as __, gettext as _
from aiogram import F

from .base_handlers import StateMassageHandler
from bot.filters import IsSubscriberCallbackFilter


common_router = Router()


@common_router.message(Command("cancel"))
@common_router.message(F.text == __("Отмена"))
@common_router.message(F.text.lower() == __("отмена"))
class CancelHandler(StateMassageHandler):
    async def handle(self) -> Any:
        await self.bot.send_message(chat_id=self.chat.id, text=_("Отмена"),
                                    reply_markup=types.ReplyKeyboardRemove())
        await self.state.clear()


@common_router.message(Command("start", "help"))
class StartHandler(StateMassageHandler):
    async def handle(self) -> Any:
        await self.bot.send_message(chat_id=self.chat.id,
                                    text=_(
                                        "Привет. С помощью этого бота ты можешь "
                                        "скачать любую песню из ВК. "
                                        "Для этого напиши мне название или "
                                        "автора композиции или просто скинь "
                                        "ссылку. По всем вопросам пишите на "
                                        "yshhenyaev@mail.ru \n"
                                        "Для смены языка пропишите /language ."))


@common_router.callback_query(F.text == "check_subscribe",
                              IsSubscriberCallbackFilter())
class StartCallbackHandler(CallbackQueryHandler):
    async def handle(self) -> Any:
        await self.bot.send_message(chat_id=self.event.message.chat.id,
                                    text=_(
                                        "Привет. С помощью этого бота ты можешь "
                                        "скачать любую песню из ВК."
                                        "Для этого напиши мне название или"
                                        "автрора композиции или просто скинь "
                                        "ссылку. По всем вопросам пишите на "
                                        "yshhenyaev@mail.ru \n"
                                        "Для смены языка пропишите \n/language ."))
