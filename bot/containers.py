from dependency_injector import containers, providers
from bot.services import VKTrackByTextService, VKTrackByIDService
from bot.repositories import VKRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["config.yml"])
    wiring_config = containers.WiringConfiguration(modules=
                                                   [".handlers.vk.song_search",
                                                    ".handlers.vk.song_by_url"
                                                    ])
    vk_repository = providers.Factory(VKRepository,
                                      access_token=config.VK_TOKEN)
    vk_service = providers.Factory(VKTrackByTextService,
                                   repository=vk_repository)
    vk_track_by_id_service = providers.Factory(VKTrackByIDService,
                                               repository=vk_repository)

class TestContainer(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["../config.yml"])
    vk_repository = providers.Factory(VKRepository,
                                      access_token=config.VK_TOKEN)
    vk_track_by_text_service = providers.Factory(VKTrackByTextService,
                                                 repository=vk_repository)
    vk_track_by_id_service = providers.Factory(VKTrackByIDService,
                                               repository=vk_repository)
