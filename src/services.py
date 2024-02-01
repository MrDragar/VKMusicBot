import asyncio
from abc import ABC

from .repositories import (VKTrackRepository, Track, TrackArray, VKRepository,
                           VKPlaylistRepository, Playlist, PlaylistArray)


class VKService(ABC):
    _repository: VKRepository

    def __init__(self, repository: VKRepository):
        self._repository = repository

    def _close_repository(self, repository: VKRepository):
        loop = asyncio.get_event_loop()
        try:
            loop.create_task(repository.close())
        except Exception as e:
            import logging
            logging.exception(e)

    def __del__(self) -> None:
        self._close_repository(self._repository)


class VkTrackService(VKService):
    _repository: VKTrackRepository

    def __init__(self, repository: VKTrackRepository):
        super().__init__(repository=repository)

    async def _add_capture(self, track: Track) -> Track:
        if not track.artist_id:
            return track
        orig_track = await self._repository.get_original_track(track.artist_id,
                                                               track.title)
        track.capture_url = await \
            self._repository.get_capture_link(owner_id=orig_track.owner_id,
                                              audio_id=orig_track.id)
        return track


class VKTrackByTextService(VkTrackService):
    async def get_track(self, q: str, i: int, offset: int = 0) -> Track:
        track_list = await self._repository.search(q=q, count=10,
                                                   offset=offset)
        track = track_list.tracks[i % 10]
        track = await self._add_capture(track)
        return track

    async def search_tracks(self, q: str, offset: int = 0) -> TrackArray:
        result = await self._repository.search(q=q, count=10,
                                               offset=offset * 10)
        return result


class VKTrackByIDService(VkTrackService):
    _repository: VKTrackRepository

    async def get_track(self, owner_id: int, audio_id: int) -> Track:
        track = await self._repository.get_by_id(owner_id, audio_id)
        track = await self._add_capture(track)
        return track


class VKPlaylistService(VKService):
    _repository: VKPlaylistRepository
    _track_repository: VKTrackRepository

    def __init__(self, playlist_repository: VKPlaylistRepository,
                 track_repository: VKTrackRepository):
        super().__init__(repository=playlist_repository)
        self._track_repository = track_repository

    async def search_playlist(self, q: str, offset: int = 0) -> PlaylistArray:
        playlist_array = await self._repository.search(q=q, offset=offset,
                                                       count=10)
        return playlist_array

    async def get_playlist(self, owner_id: int, playlist_id: int) -> Playlist:
        playlist = await self._repository.get_by_id(owner_id, playlist_id)
        await self._repository.add_tracks_to_playlist(playlist, owner_id,
                                                      playlist_id)
        return playlist

    def __del__(self) -> None:
        print(self._repository, self._track_repository)
        self._close_repository(self._track_repository)
        super().__del__()
