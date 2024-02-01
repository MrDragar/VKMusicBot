from aiogram.dispatcher.router import Router
from aiogram.filters import Command

from src.handlers.base_handlers import StateMassageHandler
from src.states import EditAdvertTotalNumberState
from src.database.advert import edit_advert_total_number

edit_total_number_router = Router()


@edit_total_number_router.message(Command("edit_advert_total_number"))
class EditTextHandler(StateMassageHandler):
    async def handle(self):
        await self.state.set_state(EditAdvertTotalNumberState.step1)
        await self.bot.send_message(chat_id=self.chat.id,
                                    text="Напишите id рекламы")


@edit_total_number_router.message(EditAdvertTotalNumberState.step1)
class GetIdHandler(StateMassageHandler):
    async def handle(self):
        if not self.event.text.isdigit():
            return self.bot.send_message(chat_id=self.chat.id,
                                         text="Ты знаешь, что такое число?")

        await self.state.update_data({"advert_id": int(self.event.text)})
        await self.state.set_state(EditAdvertTotalNumberState.step2)
        await self.bot.send_message(chat_id=self.chat.id,
                                    text="Напишите новое максимальное "
                                         "количество просмотров для рекламы")


@edit_total_number_router.message(EditAdvertTotalNumberState.step2)
class GetNewTextHandler(StateMassageHandler):
    async def handle(self):
        if not self.event.text.isdigit():
            return self.bot.send_message(chat_id=self.chat.id,
                                         text="Ты знаешь, что такое число?")

        advert_id = (await self.state.get_data())["advert_id"]
        error = await edit_advert_total_number(advert_id=advert_id,
                                               total_number=int(
                                                   self.event.text))

        await self.state.clear()
        if error:
            return self.bot.send_message(chat_id=self.chat.id,
                                         text="Нет такой партии")
        return self.bot.send_message(chat_id=self.chat.id,
                                     text="Количество просмотров успешно "
                                          "обновлено")
