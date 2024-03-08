import random

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from src.services.get_words import get_quiz
from src.view.dispatcher import dp, db
from src.view.states import StartQuiz


@dp.message(Command('start_quiz'))
async def command_start_quiz_handler(message: Message, state: FSMContext) -> None:
    """Command to start quiz. Bot gives a word, and gives variants of translate
     with one correct answer"""
    await state.set_state(StartQuiz.word)

    all_words = await db.get_random_word()
    word, options = await get_quiz(all_words)

    await state.update_data(correct_answer=options[0])
    await state.update_data(word=word.title())
    markup = await _get_markup(options)
    await message.answer(word.title(), reply_markup=markup)


@dp.message(StartQuiz.word)
async def process_start_quiz_handler(message: Message, state: FSMContext) -> None:
    """Check if chosen answer is correct or not"""
    data = await state.get_data()
    correct_answer: str = data.get('correct_answer')
    word = data.get('word')

    if message.text.lower() == correct_answer:
        await message.answer('✅ Doğru')
        await db.decrease_weight(correct_answer)
    else:
        await message.answer(f'❌ Yanlış -> doğrusu <b>{word} - {correct_answer.title()}</b>')
        await db.increase_weight(correct_answer)

    await state.clear()
    await command_start_quiz_handler(message, state)


async def _get_markup(options: list[str]) -> ReplyKeyboardMarkup:
    """Makes markup with variants"""
    options = list(set(options))
    keyboard = []
    for i in range(0, len(options), 2):
        variants = [KeyboardButton(text=options[i].title()), KeyboardButton(text=options[i+1].title())] \
            if i + 1 < len(options) else [KeyboardButton(text=options[i].title())]
        keyboard.append(variants)

    random.shuffle(options)
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
