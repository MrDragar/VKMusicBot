from aiogram.dispatcher.router import Router

from . import post
from . import statistic
from . import advert
from src.filters import IsAdmin

router = Router()

router.message.filter(IsAdmin())

router.include_router(post.router)
router.include_router(statistic.router)
router.include_router(advert.router)
