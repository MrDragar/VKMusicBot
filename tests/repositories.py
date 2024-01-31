import asyncio

from bot.repositories import Track, VKPlaylistRepository
from bot.containers import TestContainer

import unittest


class TestVKTrackByTextService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.container = TestContainer()
        self.repository: VKPlaylistRepository = self.container.vk_playlist_repository()

    async def asyncTearDown(self):
        await self.repository.close()
        del self.container
        await asyncio.sleep(0.250)

    async def test_get_playlist_by_id(self):
        """https://vk.com/music/album/-2000762159_7762159_ae3f5ac7d64a1d0fc7"""
        playlist1 = await self.repository.get_by_id(-2000762159, 7762159)
        self.assertEqual(playlist1.owner_id, -2000762159)
        self.assertEqual(playlist1.id, 7762159)
        self.assertEqual(playlist1.title, '10 V1.1.0')
        self.assertEqual(playlist1.count, 12)
        self.assertEqual(playlist1.tracks[0].id, 68231292)

        """https://vk.com/music/playlist/-147845620_930"""
        playlist2 = await self.repository.get_by_id(-147845620, 930)
        self.assertEqual(playlist2.owner_id, -147845620)
        self.assertEqual(playlist2.id, 930)
        self.assertEqual(playlist2.title, 'Плейлист твоего раздражения')
        self.assertEqual(playlist2.count, 15)
        self.assertEqual(playlist2.tracks[0].id, 456261607)

    async def test_search_playlist(self):
        playlist_array = await self.repository.search("Art of war", count=10, offset=0)
        self.assertGreater(playlist_array.count, 1)
        self.assertEqual(len(playlist_array.playlists), 10)


if __name__ == '__main__':
    unittest.main()

