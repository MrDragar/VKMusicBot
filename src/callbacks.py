from aiogram.filters.callback_data import CallbackData


class TrackCallback(CallbackData, prefix="Songs", sep=";"):
    owner_id: int
    track_id: int


class SongListCallback(CallbackData, prefix="SongList", sep=";"):
    current_offset: int
    max_offset: int


class PlaylistCallback(CallbackData, prefix="Playlist", sep=";"):
    owner_id: int
    playlist_id: int


class PlaylistListCallback(CallbackData, prefix="PlaylistList", sep=";"):
    current_offset: int
    max_offset: int
