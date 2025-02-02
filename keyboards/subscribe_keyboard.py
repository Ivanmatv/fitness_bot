from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_subscribe_keyboard():
    """
    Возвращает клавиатуру для подтверждения подписки.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Подтвердить подписку"))
    keyboard.add(KeyboardButton("Отменить подписку"))
    return keyboard
