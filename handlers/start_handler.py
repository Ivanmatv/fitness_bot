from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.main_keyboard import get_main_keyboard

router = Router(name="start_handler")

@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Добро пожаловать! Выберите действие:",
        reply_markup=get_main_keyboard()
    )

# Обработка нажатий кнопок главного меню
@router.message(lambda msg: msg.text == "Настроить профиль")
async def handle_set_profile(message: types.Message):
    from handlers.gender_handler import set_gender
    await set_gender(message)

@router.message(lambda msg: msg.text == "Получить тренировку")
async def handle_get_workout(message: types.Message, state: FSMContext):
    from handlers.sport_handler import choose_sport
    await choose_sport(message, state)

@router.message(lambda msg: msg.text == "Вернуться")
async def handle_back(message: types.Message):
    await start_command(message)