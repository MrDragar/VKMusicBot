from dependency_injector import containers, providers
from bot.services import VKService
from bot.repositories import VKRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["config.yml"])
    wiring_config = containers.WiringConfiguration(modules=
                                                   [".handlers.vk.song_search",
                                                    ".handlers.vk.song_by_url"
                                                    ])
    vk_repository = providers.Factory(VKRepository, access_token=config.VK_TOKEN)
    vk_service = providers.Factory(VKService, repository=vk_repository)


class TestContainer(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["../config.yml"])
    vk_repository = providers.Factory(VKRepository, access_token=config.VK_TOKEN)
    vk_service = providers.Factory(VKService, repository=vk_repository)
