import asyncio

from src.repositories import VKTrackRepository, Track
from src.services import (VkTrackService,
                          VKPlaylistService)
from src.containers import TestContainer

import unittest


class TestVKTrackByTextService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.container = TestContainer()
        self.service: VkTrackService = self.container.vk_track_service()

    async def test_get_track_by_id(self):
        track = await self.service.get_track(owner_id=474499121,
                                             track_id=456437231)
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


class TestVKPlaylistService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.container = TestContainer()
        self.service: VKPlaylistService = self.container.vk_playlist_service()

    async def test_search_playlist(self):
        playlist_array = await self.service.search_playlist("1", offset=0)
        self.assertGreater(playlist_array.count, 100)
        self.assertEqual(playlist_array.playlists[0].id, 10506469)
        self.assertEqual(playlist_array.playlists[0].owner_id, -2000506469)
        self.assertEqual(playlist_array.playlists[0].title, "1+1=3")
        self.assertEqual(playlist_array.playlists[0].count, 13)

    async def test_get_playlist(self):
        playlist = await self.service.get_playlist(owner_id=-2000506469,
                                                   playlist_id=10506469)
        self.assertEqual(playlist.id, 10506469)
        self.assertEqual(playlist.owner_id, -2000506469)
        self.assertEqual(playlist.title, "1+1=3")
        self.assertEqual(playlist.count, 13)

    async def asyncTearDown(self):
        del self.service
        del self.container
        await asyncio.sleep(0.250)


if __name__ == '__main__':
    unittest.main()
