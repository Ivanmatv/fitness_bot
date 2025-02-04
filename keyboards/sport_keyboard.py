# sport_keyboard.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_sport_keyboard():
    """
    Возвращает клавиатуру для выбора вида спорта.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Фитнес"))
    keyboard.add(KeyboardButton("Пауэрлифтинг"))
    keyboard.add(KeyboardButton("Кроссфит"))
    keyboard.add(KeyboardButton("Тяжёлая атлетика"))
    keyboard.add(KeyboardButton("Назад"))
    return keyboard
