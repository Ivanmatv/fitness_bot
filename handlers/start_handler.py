# start_handler.py
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.sport_keyboard import get_sport_keyboard
from keyboards.intensity_keyboard import get_intensity_keyboard
from keyboards.subscribe_keyboard import get_subscribe_keyboard
from keyboards.gender_keyboard import get_gender_keyboard
from logger import get_logger

# Получаем логгер
logger = get_logger()


async def start(message: types.Message):
    """
    Обработчик команды /start.
    Отправляет пользователю приветственное сообщение и клавиатуру с кнопками.
    """
    logger.info(f"Received /start command from user {message.from_user.id}")

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

    logger.info(f"Sent welcome message and keyboard to user {message.from_user.id}")


async def profile_handler(message: types.Message):
    logger.info("User pressed 'Настроить профиль'")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    profile_button_1 = KeyboardButton("Изменить пол")
    profile_button_2 = KeyboardButton("Изменить вид спорта")
    profile_button_3 = KeyboardButton("Изменить уровень нагрузки")
    keyboard.add(profile_button_1, profile_button_2, profile_button_3)

    await message.answer("Выберите, что хотите изменить:", reply_markup=keyboard)


async def change_gender(message: types.Message):
    """
    Обработчик выбора пола.
    """
    logger.info("User pressed 'Изменить пол'")

    # Используем функцию для получения клавиатуры
    gender_keyboard = get_gender_keyboard()
    await message.answer("Пожалуйста, выберите свой пол:", reply_markup=gender_keyboard)

    logger.info(f"Sent gender selection keyboard to user {message.from_user.id}")


async def change_sport(message: types.Message):
    """
    Обработчик выбора вида спорта.
    """
    logger.info("User pressed 'Изменить вид спорта'")

    # Используем функцию для получения клавиатуры
    sport_keyboard = get_sport_keyboard()
    await message.answer("Пожалуйста, выберите вид спорта:", reply_markup=sport_keyboard)

    logger.info(f"Sent sport selection keyboard to user {message.from_user.id}")


async def change_intensity(message: types.Message):
    """
    Обработчик выбора уровня нагрузки.
    """
    logger.info("User pressed 'Изменить уровень нагрузки'")

    # Используем функцию для получения клавиатуры
    intensity_keyboard = get_intensity_keyboard()
    await message.answer("Пожалуйста, выберите уровень нагрузки:", reply_markup=intensity_keyboard)

    logger.info(f"Sent intensity selection keyboard to user {message.from_user.id}")
