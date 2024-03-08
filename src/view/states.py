from aiogram.fsm.state import State, StatesGroup


class AddNewWord(StatesGroup):
    word = State()


class StartQuiz(StatesGroup):
    word = State()
