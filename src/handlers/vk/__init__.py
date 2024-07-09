from aiogram.dispatcher.router import Router

from src.filters import IsAdmin
from . import song_by_url
from . import song_search
from . import playlist_search
from . import playlist_by_url

router = Router()

router.message.filter(IsAdmin())

router.include_router(song_by_url.router)
router.include_router(playlist_by_url.router)
router.include_router(playlist_search.router)
router.include_router(song_search.router)
