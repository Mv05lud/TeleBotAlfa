import aiogram
import sqlalchemy
from aiogram import Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
import sqlite3
from config import dp, bot
from models import session, Formula


from aiogram.dispatcher.filters.state import State, StatesGroup


class ParamsState(StatesGroup):
    set_r = State()
    set_c = State()
    set_u = State()
    set_l = State()


async def get_button_group(data: list):
    types.ReplyKeyboardRemove()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*data)
    return keyboard


def get_available_variations() -> list:
    variations = []
    for records in session.execute(sqlalchemy.select(Formula)).fetchall():
        for record in records:
            variations.append(record.name)
    return variations


def get_menu() -> list:
    return [f"Вариант-{n}" for n in range(1, 6)]


class Messages:

    @staticmethod
    async def select_variation(message: types.Message):
        record = session.query(Formula).filter(Formula.name == message.text)  # TODO
        record = session.execute(record).fetchone()  # TODO
        await bot.send_photo(message.chat.id, record[0].schema, caption="Схема")
        await bot.send_photo(message.chat.id, record[0].formula, caption="Формула")
        await bot.send_message(message.chat.id, record[0].text_formula)
        await message.answer("Введите сопротивление 'R':")
        await ParamsState.set_r.set()


class ManagerStates:

    @staticmethod
    async def set_r(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["r"] = message.text
        await message.answer("Введите емкость 'C':")
        await ParamsState.next()

    @staticmethod
    async def set_c(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["c"] = message.text
        await message.answer("Введите напряжение 'U':")
        await ParamsState.next()

    @staticmethod
    async def set_u(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["u"] = message.text
        await message.answer("Введите индуктивность 'L':")
        await ParamsState.next()

    @staticmethod
    async def set_l(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["l"] = message.text
            await message.answer(f"Ваши параметры: r = {data['r']} c = {data['c']} u = {data['u']} l = {data['l']}")
        await state.finish()
        """Добавить код для вывода графика"""


class Commands:

    @staticmethod
    async def cmd_start(message: types.Message):
        buttons = await get_button_group(data=get_menu())
        await message.answer("Hi there", reply_markup=buttons)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(Commands.cmd_start, commands=['start'], state=None)
    dp.register_message_handler(Messages.select_variation, aiogram.dispatcher.filters.Text(equals=get_available_variations()), state=None)
    dp.register_message_handler(ManagerStates.set_r, state=ParamsState.set_r)
    dp.register_message_handler(ManagerStates.set_c, state=ParamsState.set_c)
    dp.register_message_handler(ManagerStates.set_u, state=ParamsState.set_u)
    dp.register_message_handler(ManagerStates.set_l, state=ParamsState.set_l)
