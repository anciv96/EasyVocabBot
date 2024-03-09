from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.view.dispatcher import dp, db
from src.view.states import AddNewWord


@dp.message(Command('add_new_word'))
async def command_add_new_word_handler(message: Message, state: FSMContext) -> None:
    """Command to add new word to database in format word-translate"""
    await message.answer(f'<b>kelime - çeviri</b> şeklinde yeni bir kelime yazın')
    await state.set_state(AddNewWord.word)


@dp.message(AddNewWord.word)
async def process_add_new_word_handler(message: Message, state: FSMContext) -> None:
    """Got data to add, so adding process"""
    await state.set_state(AddNewWord.word)
    try:
        await _check_word_correctness(message.text)
    except AssertionError as error:
        await message.answer(f'Ошибка формата сообщения: {error}')

    word, translate = await _convert_text_to_object(message.text)

    if not (await db.check_if_word_exists(word)):
        await db.add_word(word, translate)
        await message.answer(f'Kelime tabanına eklendi ☑️ : <b>{word}</b>')
    else:
        await message.answer(f'{word} zaten tabanda var')

    await state.clear()


async def _check_word_correctness(message_text: str) -> None:
    assert isinstance(message_text, str) is True
    part = message_text.split('-')
    assert len(part) == 2


async def _convert_text_to_object(message_text: str) -> list[str]:
    return [part.strip().lower() for part in message_text.split('-')]
