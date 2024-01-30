import asyncio

from bot.repositories import VKRepository, Track
from bot.services import VKTrackByTextService, VKTrackByIDService
from bot.containers import TestContainer

import unittest


class TestVKService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.container = TestContainer()
        self.service: VKTrackByTextService = self.container.vk_track_by_text_service()

    async def test_get_track_by_text(self):
        track_list = await self.service.search_tracks(q='Линукс',
                                                      offset=0)
        [self.assertIsInstance(i, Track) for i in track_list.tracks]
        self.assertGreater(track_list.count, 1)

    async def test_get_playlist(self):
        """https://vk.com/music/album/-2000762159_7762159_ae3f5ac7d64a1d0fc7"""
        await self.service._repository.get_playlist_by_id(-2000762159, 7762159,
                                                          count=9, offset=0)

    async def asyncTearDown(self):
        del self.service
        del self.container
        await asyncio.sleep(0.250)


class TestVKTrackByTextService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.container = TestContainer()
        self.service: VKTrackByIDService = self.container.vk_track_by_id_service()

    async def test_get_track_by_id(self):
        track = await self.service.get_track(owner_id=474499121,
                                             audio_id=456437231)
        self.assertIsInstance(track, Track)
        self.assertEqual(track.id, 456437231)
        self.assertEqual(track.owner_id, 474499121)
        self.assertEqual(track.title, "Надо было ставить линукс")
        self.assertEqual(track.artist_id, "340683553717276761")
        self.assertEqual(track.artist_name, "Научно-технический Рэп")
        self.assertEqual(track.capture_url,
                         "https://sun9-35.userapi.com/impf/c858216/v858216298/20fc69/lellIqpR8yU.jpg?size=400x400&quality=96&sign=52f0d3895ae95abe6804137109d42d96&type=audio")

    async def asyncTearDown(self):
        del self.service
        del self.container
        await asyncio.sleep(0.250)


if __name__ == '__main__':
    unittest.main()
