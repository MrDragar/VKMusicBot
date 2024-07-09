import re
from typing import Any

from aiogram import F
from aiogram import Router
from aiogram.handlers import MessageHandler
from aiogram.utils.i18n import gettext as _
from dependency_injector.wiring import Provide, inject

from src.containers import Container
from src.keyboards import get_playlist_keyboard
from src.services import VKPlaylistService

router = Router()


@router.message(F.text.regexp(r"https?://vk.com/music/album/-?[\d_]+"))
@router.message(F.text.regexp(r"https?://vk.com/music/playlist/-?[\d_]+"))
class SendPlaylistByUrlHandler(MessageHandler):
    @inject
    async def handle(
            self,
            vk_service: VKPlaylistService = Provide[
                Container.vk_playlist_service]
    ) -> Any:
        owner_id, audio_id, hash_id = re.search(
            r"-?[\d_]+", string=self.event.text
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
