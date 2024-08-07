from aiogram.utils.i18n import gettext as _
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove

from src.database.models import Language
from src.states import ChangingLanguageState
from .base_handlers import StateMassageHandler
from src.database.user import change_language
from src.keyboards import get_language_keyboard
from src.commands import set_commands_for_user

router = Router()


@router.message(Command("language"))
class ShowLanguagesHandler(StateMassageHandler):
    async def handle(self):
        await self.bot.send_message(chat_id=self.chat.id,
                                    text=_("Выберите язык"),
                                    reply_markup=get_language_keyboard())
        await self.state.set_state(ChangingLanguageState.step)


@router.message(ChangingLanguageState.step)
class GetLanguageHandler(ShowLanguagesHandler):
    async def handle(self):
        language_code = Language.get_language_code(self.event.text)
        if not language_code:
            return
        await change_language(self.event.from_user.id, language_code)
        await self.bot.send_message(chat_id=self.chat.id,
                                    text=_("Вы успешно сменили язык",
                                           locale=language_code),
                                    reply_markup=ReplyKeyboardRemove())
        await self.state.clear()
        await set_commands_for_user(self.bot, language_code, self.from_user.id,
                                    self.data["container"])


def useless_function_for_babel():
    """pybabel не видит использование lazy_gettext, поэтому тут продублирован
     текст для lazy_gettext"""
    _("отмена")
