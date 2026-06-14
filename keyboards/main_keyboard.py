from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard():
    """
    Возвращает главную клавиатуру с кнопками старта.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=
            [
                [
                KeyboardButton(text="Настроить профиль"),
                KeyboardButton(text="Получить тренировку"),
                KeyboardButton(text="Вернуться")
                ]
            ],
        resize_keyboard=True
    )
    return keyboard
