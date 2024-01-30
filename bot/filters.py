from aiogram.filters import Filter
from aiogram.types import Message, ChatMemberOwner, ChatMemberAdministrator, \
    CallbackQuery, ChatMemberMember
from aiogram.methods import GetChatMember

# from bot.config import ADMINS_ID, CHANNEL_ID
from bot.containers import Container


class IsAdmin(Filter):
    async def __call__(self, message: Message, container: Container) -> bool:
        return message.from_user.id in container.config.ADMINS_ID()


class IsSubscriberFilter(Filter):
    async def __call__(self, message: Message, container: Container) -> bool:
        member = await message.bot(GetChatMember(chat_id=container.config.CHANNEL_ID(),
                                                 user_id=message.from_user.id))
        return isinstance(member, (ChatMemberMember,
                                   ChatMemberAdministrator, ChatMemberOwner))


class IsSubscriberCallbackFilter(Filter):
    async def __call__(self, callback: CallbackQuery, container: Container) -> bool:
        member = await callback.bot(GetChatMember(chat_id=container.config.CHANNEL_ID(),
                                                  user_id=callback.from_user.id))
        return isinstance(member, (ChatMemberMember,
                                   ChatMemberAdministrator, ChatMemberOwner))
