from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.main_keyboard import get_main_keyboard
from keyboards.sport_keyboard import get_sport_keyboard
from keyboards.intensity_keyboard import get_intensity_keyboard
from keyboards.subscribe_keyboard import get_subscribe_keyboard


async def start(message: types.Message):
    """
    Обработчик команды /start.
    Отправляет пользователю приветственное сообщение и клавиатуру с кнопками.
    """
    welcome_text = (
        "Привет! Добро пожаловать в Fitness Bot.\n\n"
        "Вы можете настроить профиль, выбрать вид спорта или получить тренировку.\n"
        "Если что-то выбрано неверно — используйте кнопку 'Вернуться'."
    )

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Настроить профиль"))
    keyboard.add(KeyboardButton("Получить тренировку"))
    keyboard.add(KeyboardButton("Вернуться"))

    await message.answer(welcome_text, reply_markup=keyboard)


async def start_command_handler(message: types.Message):
    main_kb = get_main_keyboard()
    await message.answer(
        "Добро пожаловать! Выберите действие:",
        reply_markup=main_kb
    )


async def set_sport(message: types.Message):
    sport_keyboard = get_sport_keyboard()
    await message.answer("Выберите ваш вид спорта:", reply_markup=sport_keyboard)


async def set_intensity(message: types.Message):
    intensity_keyboard = get_intensity_keyboard()
    await message.answer("Выберите уровень нагрузки для тренировки:", reply_markup=intensity_keyboard)


async def ask_subscription(message: types.Message):
    subscribe_keyboard = get_subscribe_keyboard()
    await message.answer("Хотите ли вы подтвердить подписку?", reply_markup=subscribe_keyboard)
