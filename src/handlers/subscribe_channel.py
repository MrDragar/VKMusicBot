from typing import Any

from aiogram.dispatcher.router import Router
from aiogram.handlers import MessageHandler, CallbackQueryHandler
from aiogram import F
from aiogram.utils.i18n import gettext as _

from src.filters import IsSubscriberFilter, IsSubscriberCallbackFilter
from src.keyboards import get_share_link_keyboard

router = Router()


@router.message(~IsSubscriberFilter())
class ShareLinkHandler(MessageHandler):
    async def handle(self) -> Any:
        await self.bot.send_message(chat_id=self.chat.id,
                                    text=_("Для работы бота сперва необходимо"
                                           " подписаться на наш канал"),
                                    reply_markup=get_share_link_keyboard())


@router.callback_query(F.text == "check_subscribe",
                       ~IsSubscriberCallbackFilter())
class ShareLinkCallbackHandler(CallbackQueryHandler):
    async def handle(self) -> Any:
        await self.bot.send_message(chat_id=self.message.chat.id,
                                    text=_("Для работы бота сперва необходимо"
                                           " подписаться на наш канал"),
                                    reply_markup=get_share_link_keyboard())
