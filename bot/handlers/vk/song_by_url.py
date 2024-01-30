from typing import Any, List
import re

from aiogram.handlers import MessageHandler
from aiogram import Router
from aiogram import types, F
from aiogram.filters import invert_f
from aiogram.utils.i18n import lazy_gettext as __, gettext as _
from vkpymusic import ServiceAsync, Song
from dependency_injector.wiring import inject, Provide
from aiogram.types import URLInputFile

from bot.states import GetSongNameState
from bot.handlers.base_handlers import StateMassageHandler
from bot.keyboards import get_songs_keyboard
from bot.callbacks import SongCallback, SongListCallback
from bot.containers import Container
from bot.services import VKTrackByTextService

song_by_url_router = Router()


@song_by_url_router.message(F.text.regexp(r"https?://vk.com/audio-?[\d_]+"))
@song_by_url_router.message(F.text.regexp(r"[vk.com/audio]+-?[\d_]+"))
class SendSongByUrlHandler(MessageHandler):
    async def handle(self,
                     vk_service: VKTrackByTextService = Provide[Container.vk_service]) \
            -> Any:
        owner_id, audio_id = re.search(r"-?[\d_]+",
                                       string=self.event.text).group().split("_")
        if not owner_id or not audio_id:
            await self.bot.send_message(self.event.chat.id, _("Неккоректная ссылка"))
            return
        track = await vk_service.get_song_by_id(int(owner_id), int(audio_id))
        await self.bot.send_audio(self.chat.id,
                                  audio=URLInputFile(track.url),
                                  thumbnail=URLInputFile(track.capture_url)
                                  if track.capture_url else None,
                                  title=track.title,
                                  performer=track.artist_name)
