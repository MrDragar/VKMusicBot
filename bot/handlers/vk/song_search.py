from typing import Any, List

from aiogram.handlers import CallbackQueryHandler, BaseHandler, BaseHandlerMixin
from aiogram import Router
from aiogram import types, F
from aiogram.filters import invert_f
from aiogram.utils.i18n import lazy_gettext as __, gettext as _
from dependency_injector.wiring import inject, Provide
from aiogram.types import URLInputFile

from bot.states import GetSongNameState
from bot.handlers.base_handlers import StateMassageHandler
from bot.keyboards import get_songs_keyboard
from bot.callbacks import SongCallback, SongListCallback
from bot.containers import Container
from bot.services import VKTrackByTextService

song_search_router = Router()


@song_search_router.callback_query(F.data == "song")
class GetSongNameHandler(CallbackQueryHandler):
    async def handle(self) -> Any:
        await self.bot.delete_message(self.from_user.id,
                                      self.message.message_id)
        await self.bot.send_message(chat_id=self.from_user.id,
                                    text=_(
                                        "Введите название или автора композиции"))
        await self.data["state"].set_state(GetSongNameState.step1)


@song_search_router.message(GetSongNameState.step1, F.text.len() > 40)
async def handle_too_big_text(message: types.Message):
    await message.answer(_("Строка должна сожержать не более 40 символов"))


@song_search_router.message(GetSongNameState.step1, invert_f(F.text))
async def handle_too_big_text(message: types.Message):
    await message.answer(_("Чё надо?"))


@song_search_router.message(GetSongNameState.step1)
@song_search_router.message()
class SendMusicListHandler(StateMassageHandler):
    async def handle(self,
                     vk_service: VKTrackByTextService = Provide[Container.vk_service]) \
            -> Any:
        await self.state.clear()

        track_list = await vk_service.search_tracks(q=self.event.text,
                                                    offset=0)
        if track_list.count > 100:
            count = 100
        max_offset = count // 10 + (count % 10 > 0) - 1
        songs_title = [f"[{track.duration} с] {track.artist_name} - " \
                       f"{track.title}" for track in track_list.tracks]

        keyboard = get_songs_keyboard(songs_title, 0, max_offset=max_offset)

        await self.bot.send_message(chat_id=self.chat.id,
                                    text=self.event.text,
                                    reply_markup=keyboard)


@song_search_router.callback_query(SongCallback.filter())
class SendSongByNameHandler(CallbackQueryHandler):
    callback_data: str

    @inject
    async def handle(self,
                     vk_service: VKTrackByTextService = Provide[Container.vk_service]) \
            -> Any:
        text = self.message.text
        data = SongCallback.unpack(self.callback_data)
        track = await vk_service.get_track(text, data.index,
                                           data.offset)
        await self.bot.send_audio(self.message.chat.id,
                                  audio=URLInputFile(track.url),
                                  thumbnail=URLInputFile(track.capture_url)
                                  if track.capture_url else None,
                                  title=track.title,
                                  performer=track.artist_name)


@song_search_router.callback_query(SongListCallback.filter())
class ChangePageHandler(CallbackQueryHandler):
    @inject
    async def handle(self,
                     vk_service: VKTrackByTextService = Provide[Container.vk_service]) \
            -> Any:
        data = SongListCallback.unpack(self.callback_data)
        track_list = await \
            vk_service.search_tracks(q=self.message.text,
                                     offset=data.current_offset)
        songs_title = [f"[{track.duration} с] {track.artist_name} - " \
                       f"{track.title}" for track in track_list.tracks]

        keyboard = get_songs_keyboard(songs_title,
                                      current_offset=data.current_offset,
                                      max_offset=data.max_offset)

        await self.bot.edit_message_reply_markup(chat_id=self.message.chat.id,
                                                 message_id=self.message.message_id,
                                                 reply_markup=keyboard)
