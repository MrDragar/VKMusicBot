import asyncio

from bot.repositories import VKRepository, Track
from bot.services import VKService
from bot.containers import TestContainer

import unittest


class TestVKService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.container = TestContainer()
        self.service: VKService = self.container.vk_service()

    async def test_get_track_by_text(self):
        track_list = await self.service.search_songs_by_text(q='Линукс',
                                                               offset=0)
        [self.assertIsInstance(i, Track) for i in track_list.tracks]
        self.assertGreater(track_list.count, 1)

    async def test_get_track_by_id(self):
        song = await self.service.get_song_by_id(owner_id=474499121,
                                                 audio_id=456437231)
        self.assertIsInstance(song, Track)
        self.assertEqual(song.id, 456437231)
        self.assertEqual(song.owner_id, 474499121)
        self.assertEqual(song.title, "Надо было ставить линукс")
        self.assertEqual(song.artist_id, "340683553717276761")
        self.assertEqual(song.artist_name, "Научно-технический Рэп")
        self.assertEqual(song.capture_url,
                         "https://sun9-35.userapi.com/impf/c858216/v858216298/20fc69/lellIqpR8yU.jpg?size=400x400&quality=96&sign=52f0d3895ae95abe6804137109d42d96&type=audio")
        # print(song)
    async def test_get_playlist(self):
        """https://vk.com/music/album/-2000762159_7762159_ae3f5ac7d64a1d0fc7"""
        await self.service._repository.get_playlist_by_id(-2000762159, 7762159, count=9, offset=0)

    async def asyncTearDown(self):
        del self.service
        del self.container
        await asyncio.sleep(0.250)


if __name__ == '__main__':
    unittest.main()
