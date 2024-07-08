from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _
from dependency_injector.wiring import Provide

from .base_handlers import StateMassageHandler
from src.states import FeedBackState
from ..containers import Container

router = Router()


@router.message(Command("send_feedback"))
class StartPostHandler(StateMassageHandler):
    async def handle(self):
        await self.bot.send_message(chat_id=self.chat.id,
                                    text=_("Напишите ваш отзыв"))
        await self.state.set_state(FeedBackState.step)


@router.message(FeedBackState.step)
class SendPostHandler(StateMassageHandler):
    async def handle(self, admins_id: [int] = Provide[Container.config.ADMINS_ID]):
        await self.state.clear()
        for admin_id in admins_id:
            await self.bot.forward_message(chat_id=admin_id,
                                           from_chat_id=self.chat.id,
                                           message_id=self.event.message_id)
