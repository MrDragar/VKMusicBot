from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Tuple
from parse import search as parse_search
import aiohttp
from aiohttp.web import HTTPException

from aiovk.drivers import HttpDriver
import aiovk


@dataclass
class Track:
    id: int
    owner_id: int
    title: str
    url: str
    duration: int
    artist_name: Optional[str] = None
    artist_id: Optional[int] = None
    capture_url: Optional[str] = None


@dataclass
class TrackArray:
    count: int
    tracks: List[Track]


@dataclass
class Playlist:
    id: int
    owner_id: int
    title: str
    count: int
    tracks: Optional[List[Track]] = None
    artist_name: Optional[str] = None


@dataclass
class PlaylistArray:
    count: int
    playlists: List[Playlist]


class VKRepository(ABC):
    _api: aiovk.API
    _session: aiovk.TokenSession
    _http_session: aiohttp.ClientSession
    user_agent = "KateMobileAndroid/56 lite-460 (Android 4.4.2; SDK 19; x86; unknown Android SDK built for x86; en)"

    def __init__(self, access_token: str, api_version: str = "5.131"):
        self._http_session = aiohttp.ClientSession(
            headers={'User-agent': self.user_agent})
        self._session = aiovk.TokenSession(access_token=access_token,
                                           driver=HttpDriver(
                                               session=self._http_session))
        self._session.API_VERSION = api_version
        self._api = aiovk.API(self._session)

    async def close(self):
        await self._session.close()

    @abstractmethod
    async def get_by_id(self, owner_id: int, audio_id: int):
        raise NotImplementedError

    @abstractmethod
    async def search(self, q: str, count: int, offset: int):
        raise NotImplementedError


class VKTrackRepository(VKRepository):
    async def search(self, q: str, count: int, offset: int) -> \
            TrackArray:

        data = await self._api.audio.search(q=q, count=count, offset=offset)
        return self._parse_track_array(data)

    async def get_by_id(self, owner_id: int, audio_id: int) -> Track:
        data = await self._api.audio.getById(audios=f"{owner_id}_{audio_id}")
        return self._parse_track(data[0])

    async def get_original_track(self, artist_id: int, title: str) -> Track:
        a = await self._api.audio.getAudiosByArtist(artist_id=artist_id)
        track_list = self._parse_track_array(a)
        for track in track_list.tracks:
            if track.title == title:
                return track

    async def get_capture_link(self, owner_id: int, audio_id: int) -> str:
        link = f"https://vk.com/audio{owner_id}_{audio_id}"
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
        }
        try:
            response = await self._http_session.get(link, headers=headers)
            text = await response.text()
            if "artist" in link:
                cover = parse_search("background-image: url('{}')", text)[0]
            else:
                cover = parse_search("background-image:url('{}')", text)[0]
            response = await self._http_session.get(cover, headers=headers)
            if response.status != 200:
                raise CaptureAccessException
            return cover
        except HTTPException as e:
            return ""

    @staticmethod
    def _parse_track_array(data: dict) -> TrackArray:
        tracks = [VKTrackRepository._parse_track(item) for item in
                  data["items"]]
        count = data.get("count", 0) or len(data)
        return TrackArray(count=count, tracks=tracks)

    @staticmethod
    def _parse_track(data: dict) -> Track:
        main_artist = data.get("main_artists", [None])[0]
        return Track(
            id=data["id"], owner_id=data["owner_id"], title=data["title"],
            url=data["url"], duration=data["duration"],
            artist_name=data.get("artist", None),
            artist_id=main_artist["id"] if main_artist
            else None
        )


class VKPlaylistRepository(VKRepository):
    async def add_tracks_to_playlist(self, playlist: Playlist, owner_id: int,
                                     playlist_id: int) -> None:
        """Changes playlist passed to this method"""
        track_data = await self._api.audio.get(owner_id=owner_id,
                                               playlist_id=playlist_id)
        track_array = VKTrackRepository._parse_track_array(track_data)
        playlist.tracks = track_array

    async def get_by_id(self, owner_id: int, playlist_id: int) -> Playlist:
        playlist_data = await self._api.audio.getPlaylistById(owner_id=owner_id,
                                                              playlist_id=playlist_id)

        playlist = self._parse_playlist(playlist_data)
        return playlist

    async def search(self, q: str, count: int, offset: int) -> PlaylistArray:
        data = await self._api.audio.searchAlbums(q=q, count=count,
                                                  offset=offset)
        return self._parse_playlist_array(data)

    @staticmethod
    def _parse_playlist(data: dict) -> Playlist:
        main_artist = data.get("main_artists", [None])[0]
        return Playlist(
            id=data["id"], owner_id=data["owner_id"],
            title=data["title"], count=data["count"],
            artist_name=main_artist.get("name", None) if main_artist else None
        )

    @staticmethod
    def _parse_playlist_array(data: dict) -> PlaylistArray:
        playlists = [VKPlaylistRepository._parse_playlist(item) for item in
                     data["items"]]
        return PlaylistArray(count=data["count"], playlists=playlists)


class CaptureAccessException(HTTPException):
    ...
