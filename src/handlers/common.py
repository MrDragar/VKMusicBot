from typing import Any

from aiogram import F
from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.handlers import CallbackQueryHandler
from aiogram.utils.i18n import lazy_gettext as __, gettext as _

from src.filters import IsSubscriberCallbackFilter
from .base_handlers import StateMassageHandler

router = Router()


@router.message(Command("cancel"))
@router.message(F.text == __("Отмена"))
@router.message(F.text.lower() == __("отмена"))
class CancelHandler(StateMassageHandler):
    async def handle(self) -> Any:
        await self.bot.send_message(chat_id=self.chat.id, text=_("Отмена"),
                                    reply_markup=types.ReplyKeyboardRemove())
        await self.state.clear()


@router.callback_query(F.data == "cancel")
class CancelQueryHandler(CallbackQueryHandler):
    async def handle(self) -> Any:
        await self.bot.send_message(chat_id=self.message.chat.id,
                                    text=_("Отмена"))
        await self.bot.delete_message(self.message.chat.id,
                                      self.message.message_id)


@router.message(Command("start", "help"))
class StartHandler(StateMassageHandler):
    async def handle(self) -> Any:
        await self.bot.send_message(
            chat_id=self.chat.id,
            text=_(
                "Привет. С помощью этого бота ты можешь "
                "скачать любую песню из ВК.\n"
                "Для поиска песни отправьте мне её название либо её "
                "исполнителя\n"
                "/search_song - поиск песни\n"
                "/search_playlist - поиск альбома\n"
                "Также вы сразу можете скинуть мне ссылку на нужный "
                "альбом или трек \n"
                ". По всем вопросам пишите на "
                "yshhenyaev@mail.ru \n"
                "Для смены языка пропишите /language .")
        )


@router.callback_query(F.text == "check_subscribe",
                       IsSubscriberCallbackFilter())
class StartCallbackHandler(CallbackQueryHandler):
    async def handle(self) -> Any:
        await self.bot.send_message(
            chat_id=self.message.chat.id,
            text=_(
                "Привет. С помощью этого бота ты можешь "
                "скачать любую песню из ВК.\n"
                "Для поиска песни отправьте мне её название либо её "
                "исполнителя\n"
                "/search_song - поиск песни\n"
                "/search_playlist - поиск альбома\n"
                "Также вы сразу можете скинуть мне ссылку на нужный "
                "альбом или трек.\n"
                "По всем вопросам пишите на yshhenyaev@mail.ru \n"
                "Для обратной связи пропишите /send_feedback \n"
                "Для смены языка пропишите /language .")
        )
