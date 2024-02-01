from aiogram.dispatcher.router import Router
from aiogram.filters import Command

from src.handlers.base_handlers import StateMassageHandler
from src.states import NewAdvertState
from src.database.advert import create_advert

new_router = Router()


@new_router.message(Command("new_advert"))
class CreateAdvertHandler(StateMassageHandler):
    async def handle(self):
        await self.state.set_state(NewAdvertState.step1)
        await self.bot.send_message(chat_id=self.chat.id,
                                    text="Напишите количество просмотров рекламы")


@new_router.message(NewAdvertState.step1)
class GetAdvertTotalNumberHandler(StateMassageHandler):
    async def handle(self):
        if not self.event.text.isdigit():
            return self.bot.send_message(chat_id=self.chat.id,
                                         text="Ты знаешь, что такое число?")

        await self.state.update_data({"total_number": int(self.event.text)})
        await self.state.set_state(NewAdvertState.step2)
        await self.bot.send_message(chat_id=self.chat.id,
                                    text="Напишите текст (можно прикреплять "
                                         "файлы). \n"
                                         "Для отмены пропишите /cancel")


@new_router.message(NewAdvertState.step2)
class GetAdvertTextHandler(StateMassageHandler):
    async def handle(self):
        total_number = (await self.state.get_data())["total_number"]
        advert_id = await create_advert(self.chat.id, self.event.message_id,
                                        total_number)
        await self.bot.send_message(chat_id=self.chat.id,
                                    text="Реклама была создана под номером {0}"
                                    .format(advert_id))
        await self.state.clear()
