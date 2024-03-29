from aiogram.dispatcher.router import Router
from aiogram.filters import Command

from src.handlers.base_handlers import StateMassageHandler
from src.states import EditAdvertTextState
from src.database.advert import edit_advert_text

edit_text_router = Router()


@edit_text_router.message(Command("edit_advert_text"))
class EditTextHandler(StateMassageHandler):
    async def handle(self):
        await self.state.set_state(EditAdvertTextState.step1)
        await self.bot.send_message(chat_id=self.chat.id,
                                    text="Напишите id рекламы")


@edit_text_router.message(EditAdvertTextState.step1)
class GetIdHandler(StateMassageHandler):
    async def handle(self):
        if not self.event.text.isdigit():
            return self.bot.send_message(chat_id=self.chat.id,
                                         text="Ты знаешь, что такое число?")

        await self.state.update_data({"advert_id": int(self.event.text)})
        await self.state.set_state(EditAdvertTextState.step2)
        await self.bot.send_message(chat_id=self.chat.id,
                                    text="Напишите новый текст для рекламы")


@edit_text_router.message(EditAdvertTextState.step2)
class GetNewTextHandler(StateMassageHandler):
    async def handle(self):
        advert_id = (await self.state.get_data())["advert_id"]
        error = await edit_advert_text(advert_id=advert_id,
                                       chat_id=self.chat.id,
                                       message_id=self.event.message_id)
        await self.state.clear()
        if error:
            return self.bot.send_message(chat_id=self.chat.id,
                                         text="Нет такой партии")
        return self.bot.send_message(chat_id=self.chat.id,
                                     text="Текст рекламы успешно обновлён")
