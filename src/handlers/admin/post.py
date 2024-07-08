from aiogram.methods import SendMessage, ForwardMessage, CopyMessage
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _

from src.handlers.base_handlers import StateMassageHandler
from src.states import PostingState
from src.database.user import get_users

router = Router()


@router.message(Command("post"))
class StartPostHandler(StateMassageHandler):
    async def handle(self):
        await self.bot.send_message(chat_id=self.chat.id,
                                    text=_("Напишите ваш пост"))
        await self.state.set_state(PostingState.step)


@router.message(PostingState.step)
class SendPostHandler(StateMassageHandler):
    async def handle(self):
        await self.state.clear()
        users = await get_users()
        for user in users:
            try:
                await self.bot.copy_message(chat_id=user.id,
                                            from_chat_id=self.chat.id,
                                            message_id=self.event.message_id)
            except Exception as ex:
                ...
        await self.bot.send_message(chat_id=self.chat.id,
                                    text=_("Отправка поста закончена"))
