# main_keyboard.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    """
    Возвращает главную клавиатуру с кнопками старта.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Настроить профиль"))
    keyboard.add(KeyboardButton("Получить тренировку"))
    keyboard.add(KeyboardButton("Назад"))
    return keyboard
