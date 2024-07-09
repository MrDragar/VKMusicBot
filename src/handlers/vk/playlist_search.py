from typing import Any

from aiogram import types, F, Router, flags
from aiogram.filters import invert_f, Command
from aiogram.handlers import CallbackQueryHandler
from aiogram.utils.i18n import gettext as _
from dependency_injector.wiring import Provide, inject

from src.callbacks import PlaylistListCallback, PlaylistCallback
from src.containers import Container
from src.handlers.base_handlers import StateMassageHandler
from src.keyboards import get_playlists_keyboard, get_playlist_keyboard
from src.services import VKPlaylistService
from src.states import GetPlaylistNameState

router = Router()


@router.message(Command("search_playlist"))
@flags.chat_action("typing")
class SearchPlaylistsHandler(StateMassageHandler):
    @inject
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
async def handle_no_text(message: types.Message):
    await message.answer(_("Чё надо?"))


@router.message(GetPlaylistNameState.step1)
@flags.chat_action("typing")
class SendPlaylistListHandler(StateMassageHandler):
    @inject
    async def handle(
            self,
            vk_service: VKPlaylistService = Provide[
                Container.vk_playlist_service]
    ) -> Any:
        await self.state.clear()

        playlist_list = await vk_service.search_playlist(
            q=self.event.text,
            offset=0
        )
        if playlist_list.count > 50:
            playlist_list.count = 50
        max_offset = playlist_list.count // 10 + (
                playlist_list.count % 10 > 0) - 1

        keyboard = get_playlists_keyboard(
            playlists=playlist_list.playlists,
            current_offset=0,
            max_offset=max_offset
        )
        await self.bot.send_message(
            chat_id=self.event.chat.id,
            text=self.event.text,
            reply_markup=keyboard
        )


@router.callback_query(PlaylistListCallback.filter())
@flags.chat_action("typing")
class ChangePlaylistsPageHandler(CallbackQueryHandler):
    @inject
    async def handle(
            self,
            vk_service: VKPlaylistService = Provide[
                Container.vk_playlist_service]
    ) -> Any:
        data = PlaylistListCallback.unpack(self.callback_data)

        playlist_list = await vk_service.search_playlist(
            q=self.message.text,
            offset=data.current_offset
        )

        keyboard = get_playlists_keyboard(
            playlists=playlist_list.playlists,
            current_offset=data.current_offset,
            max_offset=data.max_offset
        )

        await self.bot.edit_message_reply_markup(
            chat_id=self.message.chat.id,
            message_id=self.message.message_id,
            reply_markup=keyboard
        )


@router.callback_query(PlaylistCallback.filter())
@flags.chat_action("typing")
class SendPlaylist(CallbackQueryHandler):
    @inject
    async def handle(
            self,
            vk_service: VKPlaylistService = Provide[
                Container.vk_playlist_service]
    ) -> Any:
        data = PlaylistCallback.unpack(self.callback_data)
        playlist = await vk_service.get_playlist(
            data.owner_id,
            data.playlist_id,
            data.current_offset
        )
        if playlist.count > 100:
            playlist.count = 100
        max_offset = playlist.count // 10 + (playlist.count % 10 > 0) - 1

        keyboard = get_playlist_keyboard(playlist, data.current_offset,
                                         max_offset)
        if data.first_time:
            await self.bot.send_message(
                chat_id=self.message.chat.id,
                text=f"[{playlist.count}] {playlist.artist_name} - {playlist.title}",
                reply_markup=keyboard
            )
        else:
            await self.bot.edit_message_reply_markup(
                chat_id=self.message.chat.id,
                message_id=self.message.message_id,
                reply_markup=keyboard
            )
