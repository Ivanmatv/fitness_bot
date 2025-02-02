import logging
from aiogram import Bot, Dispatcher, types
import os

from config import API_TOKEN
from handlers import (
    start_handler,
    gender_handler,
    sport_handler,
    intensity_handler,
    workout_handler
)
from aiogram.types import ParseMode

# Проверка токена
if not API_TOKEN:
    raise ValueError("API_TOKEN is not set in environment variables or config file.")

# Инициализация бота
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

# Регистрация хендлеров / команд
dp.register_message_handler(start_handler.start, commands="start")
dp.register_message_handler(gender_handler.set_gender, commands="gender")
dp.register_message_handler(sport_handler.set_sport, commands="sport")
dp.register_message_handler(intensity_handler.set_intensity, commands="intensity")
dp.register_message_handler(workout_handler.generate_workout, commands="generate_workout")

# Регистрация callback-хендлеров
dp.register_callback_query_handler(
    gender_handler.gender_callback_handler,
    lambda c: c.data and c.data.startswith("gender_")
)
dp.register_callback_query_handler(
    sport_handler.sport_callback_handler,
    lambda c: c.data and c.data.startswith("sport_")
)
dp.register_callback_query_handler(
    intensity_handler.intensity_callback_handler,
    lambda c: c.data and c.data.startswith("intensity_")
)

# Логирование
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
