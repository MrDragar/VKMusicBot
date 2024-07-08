from aiogram.dispatcher.router import Router

from . import common
from . import language
from . import admin
from . import feedback
from . import subscribe_channel
from . import vk

router = Router()

router.include_router(subscribe_channel.router)
router.include_router(common.router)
router.include_router(language.router)
router.include_router(admin.router)
router.include_router(feedback.router)
router.include_router(vk.router)
