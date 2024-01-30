from aiogram.dispatcher.router import Router

from bot.filters import IsAdmin
from . import song_by_url
from . import song_search

vk_router = Router()

vk_router.message.filter(IsAdmin())

vk_router.include_router(song_by_url.song_by_url_router)
vk_router.include_router(song_search.song_search_router)
