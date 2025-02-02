from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_intensity_keyboard():
    """
    Возвращает клавиатуру для выбора уровня нагрузки.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Лёгкий"))
    keyboard.add(KeyboardButton("Средний"))
    keyboard.add(KeyboardButton("Тяжёлый"))
    keyboard.add(KeyboardButton("Назад"))
    return keyboard
