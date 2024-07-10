import logging
from typing import Any

from aiogram import types, F, Router
from aiogram.filters import invert_f, Command
from aiogram.handlers import CallbackQueryHandler, MessageHandler
from aiogram.types import URLInputFile
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.i18n import gettext as _
from dependency_injector.wiring import inject, Provide

from src.callbacks import TrackCallback, SongListCallback
from src.containers import Container
from src.database.day_statistic import add_download
from src.handlers.base_handlers import StateMassageHandler
from src.handlers.advert_mixins import AdvertMixin
from src.keyboards import get_songs_keyboard
from src.services import VkTrackService
from src.states import GetSongNameState

router = Router()


@router.message(Command("search_song"))
class SearchSongsHandler(MessageHandler):
    @inject
    async def handle(self):
        await self.bot.delete_message(self.from_user.id,
                                      self.event.message_id)
        await self.bot.send_message(chat_id=self.from_user.id,
                                    text=_("Введите название или автора композиции"))
        await self.data["state"].set_state(GetSongNameState.step1)


@router.message(GetSongNameState.step1, F.text.len() > 40)
async def handle_too_big_text(message: types.Message):
    await message.answer(_("Строка должна сожержать не более 40 символов"))


@router.message(GetSongNameState.step1, invert_f(F.text))
async def handle_too_big_text(message: types.Message):
    await message.answer(_("Чё надо?"))


@router.message(GetSongNameState.step1)
@router.message()
class SendMusicListHandler(StateMassageHandler):
    @inject
    async def handle(
            self,
            vk_service: VkTrackService = Provide[Container.vk_track_service]
    ) -> Any:
        await self.state.clear()

        track_list = await vk_service.search_tracks(
            q=self.event.text,
            offset=0
        )
        if track_list.count > 100:
            track_list.count = 100
        max_offset = track_list.count // 10 + (track_list.count % 10 > 0) - 1

        keyboard = get_songs_keyboard(
            track_list.tracks,
            current_offset=0,
            max_offset=max_offset
        )

        await self.bot.send_message(
            chat_id=self.chat.id,
            text=self.event.text,
            reply_markup=keyboard
        )


@router.callback_query(TrackCallback.filter())
class SendSongByNameHandler(CallbackQueryHandler, AdvertMixin):
    callback_data: str

    @inject
    async def handle(
            self,
            vk_service: VkTrackService = Provide[Container.vk_track_service]
    ) -> Any:
        text = self.message.text
        data = TrackCallback.unpack(self.callback_data)
        track = await vk_service.get_track(
            owner_id=data.owner_id,
            track_id=data.track_id
        )
        logging.debug("sending audio")
        async with ChatActionSender(bot=self.bot, chat_id=self.message.chat.id,
                                    action='upload_voice'):
            await self.bot.send_audio(
                self.message.chat.id,
                audio=URLInputFile(track.url),
                thumbnail=URLInputFile(
                    track.capture_url) if track.capture_url else None,
                title=track.title,
                performer=track.artist_name
            )
        logging.debug("end sending audio")
        await add_download()
        await self.send_advert()


@router.callback_query(SongListCallback.filter())
class ChangePageHandler(CallbackQueryHandler):
    @inject
    async def handle(
            self,
            vk_service: VkTrackService = Provide[Container.vk_track_service]
    ) -> Any:
        data = SongListCallback.unpack(self.callback_data)
        track_list = await vk_service.search_tracks(
            q=self.message.text,
            offset=data.current_offset
        )

        keyboard = get_songs_keyboard(
            track_list.tracks,
            current_offset=data.current_offset,
            max_offset=data.max_offset
        )

        await self.bot.edit_message_reply_markup(
            chat_id=self.message.chat.id,
            message_id=self.message.message_id,
            reply_markup=keyboard
        )
