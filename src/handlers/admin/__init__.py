from aiogram.dispatcher.router import Router

from . import post
from . import statistic
from . import advert
from src.filters import IsAdmin

admin_router = Router()

admin_router.message.filter(IsAdmin())

admin_router.include_router(post.post_router)
admin_router.include_router(statistic.statistic_router)
admin_router.include_router(advert.advert_router)
