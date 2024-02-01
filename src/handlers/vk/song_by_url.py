from typing import Any, List
import re

from aiogram.handlers import MessageHandler
from aiogram import Router
from aiogram import types, F
from aiogram.filters import invert_f
from aiogram.utils.i18n import lazy_gettext as __, gettext as _
from dependency_injector.wiring import inject, Provide
from aiogram.types import URLInputFile


from src.containers import Container
from src.services import VKTrackByIDService

song_by_url_router = Router()


@song_by_url_router.message(F.text.regexp(r"https?://vk.com/audio-?[\d_]+"))
@song_by_url_router.message(F.text.regexp(r"[vk.com/audio]+-?[\d_]+"))
class SendSongByUrlHandler(MessageHandler):
    async def handle(self,
                     vk_service: VKTrackByIDService =
                     Provide[Container.vk_track_by_id_service]) -> Any:
        owner_id, audio_id = re.search(r"-?[\d_]+",
                                       string=self.event.text).group().split("_")
        if not owner_id or not audio_id:
            await self.bot.send_message(self.event.chat.id, _("Неккоректная ссылка"))
            return
        track = await vk_service.get_track(int(owner_id), int(audio_id))
        await self.bot.send_audio(self.chat.id,
                                  audio=URLInputFile(track.url),
                                  thumbnail=URLInputFile(track.capture_url)
                                  if track.capture_url else None,
                                  title=track.title,
                                  performer=track.artist_name)
