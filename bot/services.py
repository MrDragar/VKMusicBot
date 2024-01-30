from typing import List, Tuple
import asyncio

from .repositories import VKRepository, Track, TrackList


class VKService:
    def __init__(self, repository: VKRepository):
        self._repository = repository

    async def get_track_by_text(self, q: str, i: int, offset: int = 0) -> Track:
        track_list = await self._repository.search_song(q=q, count=10,
                                                        offset=offset)
        track = track_list.tracks[i % 10]
        track = await self.add_capture(track)
        return track

    async def get_song_by_id(self, owner_id: int, audio_id: int) -> Track:
        track = await self._repository.get_song_by_id(owner_id, audio_id)
        track = await self.add_capture(track)
        return track

    async def search_songs_by_text(self, q: str, offset: int = 0) -> TrackList:
        result = await self._repository.search_song(q=q, count=10,
                                                    offset=offset * 10)
        return result

    async def add_capture(self, track: Track) -> Track:
        if not track.artist_id:
            return track
        orig_track = await self._repository.get_original_song(track.artist_id,
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