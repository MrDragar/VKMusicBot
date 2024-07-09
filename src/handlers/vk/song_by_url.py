import re
from typing import Any

from aiogram import F
from aiogram import Router
from aiogram.handlers import MessageHandler
from aiogram.types import URLInputFile
from aiogram.utils.i18n import gettext as _
from dependency_injector.wiring import Provide, inject

from src.containers import Container
from src.services import VkTrackService

router = Router()


@router.message(F.text.regexp(r"https?://vk.com/audio-?[\d_]+"))
@router.message(F.text.regexp(r"[vk.com/audio]+-?[\d_]+"))
class SendSongByUrlHandler(MessageHandler):
    @inject
    async def handle(
            self,
            vk_service: VkTrackService = Provide[Container.vk_track_service]
    ) -> Any:
        owner_id, audio_id = re.search(
            r"-?[\d_]+", string=self.event.text
        ).group().split("_")

        if not owner_id or not audio_id:
            await self.bot.send_message(
                self.event.chat.id,
                _("Неккоректная ссылка")
            )
            return
        track = await vk_service.get_track(int(owner_id), int(audio_id))

        await self.bot.send_audio(
            self.chat.id,
            audio=URLInputFile(track.url),
            thumbnail=URLInputFile(track.capture_url) if track.capture_url else None,
            title=track.title,
            performer=track.artist_name
        )
