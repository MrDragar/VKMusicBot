from aiogram.fsm.state import StatesGroup, State


class ChangingLanguageState(StatesGroup):
    step = State()


class FeedBackState(StatesGroup):
    step = State()


class PostingState(StatesGroup):
    step = State()


class NewAdvertState(StatesGroup):
    step1 = State()
    step2 = State()


class EditAdvertTextState(StatesGroup):
    step1 = State()
    step2 = State()


class EditAdvertTotalNumberState(StatesGroup):
    step1 = State()
    step2 = State()


class GetAdvertByIdState(StatesGroup):
    step1 = State()


class GetSongNameState(StatesGroup):
    step1 = State()
