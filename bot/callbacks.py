from aiogram.filters.callback_data import CallbackData


class SongCallback(CallbackData, prefix="Songs", sep="|\/"):
    offset: int
    index: int


class PlaylistCallback(CallbackData, prefix="Playlist", sep="|\/"):
    text: str
    ListIndex: int


class SongListCallback(CallbackData, prefix="SongList", sep="|\/"):
    current_offset: int
    max_offset: int
