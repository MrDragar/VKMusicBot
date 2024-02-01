from typing import List

from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from src.database.models import Language
from src.repositories import Track
from src.callbacks import TrackCallback, SongListCallback


def get_language_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    for language in Language:
        keyboard.button(text=language.get_language_name())

    keyboard.row(types.KeyboardButton(text=_("Отмена")))
    markup = keyboard.as_markup()
    markup.one_time_keyboard = True
    markup.resize_keyboard = True
    return markup


def get_share_link_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=_("Подписаться на канал"),
                    url="https://t.me/AudioDownloader")
    keyboard.button(text=_("Проверить подписку"),
                    callback_data="check_subscribe")
    return keyboard.as_markup()


def get_main_menu_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=_("Искать по названию песни"), callback_data="song")
    keyboard.button(text=_("Искать по плейлисту"), callback_data="playlist")
    return keyboard.as_markup()


def get_songs_keyboard(tracks: List[Track],
                       current_offset,
                       max_offset) -> types.InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for track in tracks:
        keyboard.button(text=track.title,
                        callback_data=TrackCallback(owner_id=track.owner_id,
                                                    track_id=track.id).pack())
    keyboard.adjust(1)
    keyboard.row(
        types.InlineKeyboardButton(text="0",
                                   callback_data=SongListCallback(
                                       current_offset=0,
                                       max_offset=max_offset).pack()  if current_offset > 0 else "0"
                                   ),

        types.InlineKeyboardButton(text="<",
                                   callback_data=SongListCallback(
                                       current_offset=current_offset - 1,
                                       max_offset=max_offset).pack() if current_offset > 0 else "0"
                                   ),

        types.InlineKeyboardButton(text=str(current_offset),
                                   callback_data="0"),
        types.InlineKeyboardButton(text=">",
                                   callback_data=SongListCallback(
                                       current_offset=current_offset + 1,
                                       max_offset=max_offset).pack() if current_offset < max_offset else "0"
                                   ),
        types.InlineKeyboardButton(text=str(max_offset),
                                   callback_data=SongListCallback(
                                       current_offset=max_offset,
                                       max_offset=max_offset).pack() if current_offset < max_offset else "0"
                                   ),
    )

    keyboard.row(types.InlineKeyboardButton(text=_("Отмена"),
                                            callback_data="cancel"))

    return keyboard.as_markup()
