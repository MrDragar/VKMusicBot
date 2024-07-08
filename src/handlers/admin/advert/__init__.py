from aiogram.dispatcher.router import Router

from . import new
from . import edit_text
from . import edit_total_number
from . import get

router = Router()

router.include_router(new.new_router)
router.include_router(edit_text.edit_text_router)
router.include_router(edit_total_number.edit_total_number_router)
router.include_router(get.get_router)
