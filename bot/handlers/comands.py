import asyncio

from aiogram import F, Router, html, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (FSInputFile, KeyboardButton, Message,
                           ReplyKeyboardMarkup)
from handlers.logic import insert_data, search_data

router = Router()

login = 0


class Form(StatesGroup):
    register = State()
    login = State()


@router.message(Command("start"))
async def cmd_start(message: types.Message):

    text = "Привіт, я був створений для того аби ти розібрався з пошуком замін."

    await message.answer(text)
    await asyncio.sleep(1)
    await cmd_menu(message)


@router.message(lambda message: message.text == "Меню")
async def cmd_menu(message: types.Message):
    text1 = "Будьласка оберіть потрібну вам дію"
    kb = [
        [KeyboardButton(text="Вхід")],
        [KeyboardButton(text="Реєстрація")],
        [KeyboardButton(text="Допомога")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.reply(text1, reply_markup=keyboard)


@router.message(lambda message: message.text == "Виберіть групу")
async def cmd_vibir_group(message: types.Message):
    text1 = "Будьласка оберіть потрібну вам групу, або натисніть повернутися в меню"
    kb = [
        [KeyboardButton(text="РПЗ-48")],
        [KeyboardButton(text="РПЗ-49")],
        [KeyboardButton(text="Меню")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.reply(text1, reply_markup=keyboard)


@router.message(lambda message: message.text == "Реєстрація")
async def cmd_register(message: types.Message, state: FSMContext):
    text = "Будьласка введіть email та пароль\nПриклад: test@example.com 12345678"
    await message.reply(text, reply_markup=types.ReplyKeyboardRemove())
    kb = [
        [KeyboardButton(text="Так, вірно")],
        [KeyboardButton(text="Ні, давай заново")],
        [KeyboardButton(text="Допомога")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await state.set_state(Form.register)

    @router.message(Form.register)
    async def extract_data(message: types.Message):

        try:
            text = message.text.split()
            email, password = text
            if len(text) != 2:
                asyncio.sleep(1)
                await cmd_menu(message)
                await message.reply("Непрацивлийний ввід")

            else:
                text = (email, password)
                await message.answer(
                    f"Чи все правильно?\nE-mail: {email}\nПароль: {password}",
                    reply_markup=keyboard,
                )

        except ValueError:
            await message.reply("Непрацивлийний ввід")

        @router.message(lambda message: message.text == "Так, вірно")
        async def insert_info(message: types.Message):
            global login
            sho = await insert_data(text)
            await message.answer(sho)
            login = 1
            asyncio.sleep(2)
            await cmd_vibir_group(message)

        await state.clear()


@router.message(lambda message: message.text == "Вхід")
async def cmd_vhid(message: types.Message, state: FSMContext):

    text = "Будьласка введіть email та пароль\nПриклад: test@example.com 12345678"
    await message.reply(text, reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.login)

    @router.message(Form.login)
    async def cmd_login(message: types.Message):
        data = message.text.split()
        email, password = await search_data(data)
        global login
        if email and password:
            await message.answer("👾")
            await message.answer(
                f"Користувача знайдено \nПочта: {email}\nПароль: {password}"
            )
            await state.clear()
            login = 1
            asyncio.sleep(2)
            await cmd_vibir_group(message)
        else:
            await message.answer("Користувача не знайдено")
            await cmd_menu(message)
            await state.clear()


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


@router.message(lambda message: message.text == "РПЗ-48")
async def cmd_rpz_48(message: types.Message):
    file_ids = []
    global login
    if login == 1:
        image_from_pc = FSInputFile("bot/handlers/photos/photo_2024-05-28_16-52-21.jpg")
        result = await message.answer_photo(
            image_from_pc, caption="Изображение из файла на компьютере"
        )
        file_ids.append(result.photo[-1].file_id)
        await message.answer("РПЗ-48")
    else:
        await message.answer("Ви не авторизовані")
        asyncio.sleep(1)
        await cmd_menu(message)


@router.message(lambda message: message.text == "РПЗ-49")
async def cmd_rpz_49(message: types.Message):

    await message.answer("РПЗ-48")
