import re
from typing import Any

from aiogram import F, Router
from aiogram.handlers import MessageHandler
from aiogram.types import URLInputFile, Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.i18n import gettext as _
from dependency_injector.wiring import Provide, inject

from src.containers import Container
from src.database.day_statistic import add_download
from src.keyboards import get_playlist_keyboard
from src.services import VKPlaylistService, VkTrackService
from src.handlers.advert_mixins import AdvertMixin

router = Router()


@router.message(F.text.regexp(r"https?://vk.com/music/album/-?[\d_]+"))
@router.message(F.text.regexp(r"https?://vk.com/music/playlist/-?[\d_]+"))
@router.message(F.text.regexp(
    r"https?://vk.com/audio\?z=audio_playlist-?[\d]+_-?[\d]+/\w+"))
class SendPlaylistByUrlHandler(MessageHandler):
    @inject
    async def handle(
            self,
            vk_service: VKPlaylistService = Provide[
                Container.vk_playlist_service]
    ) -> Any:
        owner_id, audio_id = re.search(
            r"-?[\d]+_-?[\d]+", string=self.event.text
        ).group().split("_")

        if not owner_id or not audio_id:
            await self.bot.send_message(
                self.event.chat.id,
                _("Неккоректная ссылка")
            )
            return
        playlist = await vk_service.get_playlist(int(owner_id), int(audio_id))
        if playlist.count > 100:
            playlist.count = 100
        max_offset = playlist.count // 10 + (playlist.count % 10 > 0) - 1

        keyboard = get_playlist_keyboard(playlist, 0, max_offset)
        await self.bot.send_message(
            chat_id=self.event.chat.id,
            text=f"[{playlist.count}] {playlist.artist_name} - {playlist.title}",
            reply_markup=keyboard
        )


@router.message(F.text.regexp(r"https?://vk.com/audio-?[\d_]+"))
@router.message(F.text.regexp(r"[vk.com/audio]+-?[\d_]+"))
class SendSongByUrlHandler(MessageHandler, AdvertMixin):
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

        async with ChatActionSender(bot=self.bot, chat_id=self.chat.id):
            await self.bot.send_audio(
                self.chat.id,
                audio=URLInputFile(track.url),
                thumbnail=URLInputFile(
                    track.capture_url) if track.capture_url else None,
                title=track.title,
                performer=track.artist_name
            )

        await add_download()
        await self.send_advert()


@router.message(F.text.regexp(r"https?://vk.com"))
async def url_handler(message: Message):
    await message.answer(_("Ссылка некорректна"))
