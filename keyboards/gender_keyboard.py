# gender_keyboard.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_gender_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Мужчина"))
    keyboard.add(KeyboardButton("Женщина"))
    keyboard.add(KeyboardButton("Назад"))
    return keyboard
