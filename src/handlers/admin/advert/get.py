from aiogram.dispatcher.router import Router
from aiogram.filters import Command

from src.handlers.base_handlers import StateMassageHandler
from src.states import GetAdvertByIdState
from src.database.advert import get_advert_by_id, get_active_adverts

get_router = Router()


@get_router.message(Command("get_advert"))
class GetActiveAdvertsHandler(StateMassageHandler):
    async def handle(self):
        await self.state.set_state(GetAdvertByIdState.step1)
        await self.bot.send_message(chat_id=self.chat.id,
                                    text="Напишите id рекламы")


@get_router.message(GetAdvertByIdState.step1)
class GetIdHandler(StateMassageHandler):
    async def handle(self):
        if not self.event.text.isdigit():
            return self.bot.send_message(chat_id=self.chat.id,
                                         text="Ты знаешь, что такое число?")
        advert = await get_advert_by_id(int(self.event.text))
        await self.state.clear()

        if not advert:
            return self.bot.send_message(chat_id=self.chat.id,
                                         text="Нет такой партии")

        await self.bot.send_message(chat_id=self.chat.id,
                                    text="id: {0} \n"
                                         "Количество просмотров: {1} \n"
                                         "Максимальное количество просмотров: {2}\n"
                                         "Текст:".format(advert.id,
                                                         advert.current_number,
                                                         advert.total_number))
        await self.bot.copy_message(chat_id=self.chat.id,
                                    from_chat_id=advert.chat_id,
                                    message_id=advert.message_id)


@get_router.message(Command("get_active_adverts"))
class GetActiveAdvertHandler(StateMassageHandler):
    async def handle(self):
        adverts = await get_active_adverts()
        if not adverts:
            return self.bot.send_message(chat_id=self.chat.id,
                                         text="Нет активных реклам")

        text = "Id активных реклам: \n"
        for advert in adverts:
            text += f"{advert.id}, "
        text = text[:-2]
        await self.bot.send_message(chat_id=self.chat.id, text=text)
