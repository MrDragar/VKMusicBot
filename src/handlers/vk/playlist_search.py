from typing import Any, List

from aiogram.handlers import CallbackQueryHandler, MessageHandler
from aiogram import types, F, Router
from aiogram.filters import invert_f, Command
from aiogram.utils.i18n import lazy_gettext as __, gettext as _
from dependency_injector.wiring import inject, Provide
from aiogram.types import URLInputFile

from src.states import GetPlaylistNameState
from src.handlers.base_handlers import StateMassageHandler
from src.keyboards import get_songs_keyboard
from src.callbacks import TrackCallback, SongListCallback
from src.containers import Container
from src.services import VkTrackService, VKTrackRepository, VKPlaylistService

router = Router()


@router.message(Command("search_playlist"))
class SearchPlaylistsHandler(StateMassageHandler):
    async def handle(self) -> Any:
        await self.bot.delete_message(self.from_user.id,
                                      self.event.message_id)
        await self.bot.send_message(chat_id=self.from_user.id,
                                    text=_(
                                        "Введите название или автора альбома"))
        await self.data["state"].set_state(GetPlaylistNameState.step1)


@router.message(GetPlaylistNameState.step1, F.text.len() > 40)
async def handle_too_big_text(message: types.Message):
    await message.answer(_("Строка должна сожержать не более 40 символов"))


@router.message(GetPlaylistNameState.step1, invert_f(F.text))
async def handle_too_big_text(message: types.Message):
    await message.answer(_("Чё надо?"))


@router.message(GetPlaylistNameState.step1)
class SendPlaylistListHandler(StateMassageHandler):
    async def handle(
            self,
            vk_service: VKPlaylistService = Provide[Container.vk_playlist_service]
    ) -> Any:
        print(vk_service)
        playlist_list = await vk_service.search_playlist(
            q=self.event.text,
            offset=0
        )
