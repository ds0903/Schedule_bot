import asyncio

from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):

    text = "Привіт, я був створений для того аби ти розібрався з пошуком замін."
    text1 = "будьласка оберіть потрібну вам дію"

    kb = [
        [KeyboardButton(text="Вхід")], [KeyboardButton(text="Реєстарція")], [KeyboardButton(text="Допомога")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(text)
    await asyncio.sleep(1)
    await message.answer(text1, reply_markup=keyboard)

@router.message(lambda message: message.text == "Меню")
async def show_menu(message: types.Message):

    await cmd_start(message)

@router.message(Command("Вхід"))
async def cmd_register(message: types.Message):

    await message.answer("text_vhid")

@router.message(Command("Реєстрація"))
async def cmd_register(message: types.Message):

    await message.answer("text_register")


@router.message(lambda message: message.text == "Допомога")
async def cmd_dopomoga(message: types.Message):
    text = str(
        "Ви можете звернутися за допомогою до розрозбника @ds0903",
    )
    await message.reply(text, reply_markup=types.ReplyKeyboardRemove())
    kb = [
        [KeyboardButton(text="Меню")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await asyncio.sleep(2)
    await message.answer("абож ви можете повернутися в меню", reply_markup=keyboard)