from aiogram.dispatcher.router import Router

from . import song_search
from . import playlist_search
from . import send_by_url
from . import errors

router = Router()

router.include_router(errors.router)
router.include_router(send_by_url.router)
router.include_router(playlist_search.router)
router.include_router(song_search.router)
