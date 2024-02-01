from src.services import (VKTrackByTextService, VKTrackByIDService,
                          VKPlaylistService)
from src.repositories import VKTrackRepository, VKPlaylistRepository

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["config.yml"])
    wiring_config = containers.WiringConfiguration(modules=
                                                   [".handlers.vk.song_search",
                                                    ".handlers.vk.song_by_url"
                                                    ])
    vk_track_repository = providers.Factory(VKTrackRepository,
                                            access_token=config.VK_TOKEN)
    vk_playlist_repository = providers.Factory(VKPlaylistRepository,
                                               access_token=config.VK_TOKEN)
    vk_track_by_text_service = providers.Factory(VKTrackByTextService,
                                                 repository=vk_track_repository)
    vk_track_by_id_service = providers.Factory(VKTrackByIDService,
                                               repository=vk_track_repository)


class TestContainer(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["../config.yml"])
    vk_track_repository = providers.Factory(VKTrackRepository,
                                            access_token=config.VK_TOKEN)
    vk_playlist_repository = providers.Factory(VKPlaylistRepository,
                                               access_token=config.VK_TOKEN)

    vk_track_by_text_service = providers.Factory(VKTrackByTextService,
                                                 repository=vk_track_repository)
    vk_track_by_id_service = providers.Factory(VKTrackByIDService,
                                               repository=vk_track_repository)
    vk_playlist_service = providers.Factory(
        VKPlaylistService,
        track_repository=vk_track_repository,
        playlist_repository=vk_playlist_repository
    )