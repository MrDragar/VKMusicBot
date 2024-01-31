import asyncio
from abc import ABC

from .repositories import VKTrackRepository, Track, TrackArray


class VkService(ABC):
    _repository: VKTrackRepository

    def __init__(self, repository: VKTrackRepository):
        self._repository = repository

    async def _add_capture(self, track: Track) -> Track:
        if not track.artist_id:
            return track
        orig_track = await self._repository.get_original_track(track.artist_id,
                                                               track.title)
        track.capture_url = await \
            self._repository.get_capture_link(owner_id=orig_track.owner_id,
                                              audio_id=orig_track.id)
        return track

    def __del__(self) -> None:
        loop = asyncio.get_event_loop()
        try:
            loop.create_task(self._repository.close())
        except Exception as e:
            import logging
            logging.exception(e)


class VKTrackByTextService(VkService):
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


class VKTrackByIDService(VkService):
    async def get_track(self, owner_id: int, audio_id: int) -> Track:
        track = await self._repository.get_by_id(owner_id, audio_id)
        track = await self._add_capture(track)
        return track


class VKByPlaylistService(VkService):
    ...
