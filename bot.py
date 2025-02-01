from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging

from config import API_TOKEN
from handlers import start_handler, gender_handler, sport_handler, intensity_handler, workout_handler
from payments import crypto_payment

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Регистрация обработчиков
dp.register_message_handler(start_handler.start, commands="start")
dp.register_message_handler(gender_handler.set_gender, commands="gender")
dp.register_message_handler(sport_handler.set_sport, commands="sport")
dp.register_message_handler(intensity_handler.set_intensity, commands="intensity")
dp.register_message_handler(workout_handler.generate_workout, commands="generate_workout")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
