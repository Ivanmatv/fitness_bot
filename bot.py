from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton

from config import API_TOKEN
from handlers import start_handler, gender_handler, sport_handler, intensity_handler, workout_handler
# from payments import crypto_payment
from logger import get_logger

# Создаем логгер
logger = get_logger()

# Проверка токена
if not API_TOKEN:
    logger.error("API_TOKEN is not set in environment variables or config file.")
    raise ValueError("API_TOKEN is not set in environment variables or config file.")

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Регистрация обработчиков команд
handlers_list = [
    (start_handler.start, "start"),
    (gender_handler.set_gender, "gender"),
    (sport_handler.set_sport, "sport"),
    (intensity_handler.set_intensity, "intensity"),
    (workout_handler.generate_workout, "generate_workout"),
]

for handler, command in handlers_list:
    dp.register_message_handler(handler, commands=command)


# Обработчик кнопки "Настроить профиль"
@dp.message_handler(lambda message: message.text == "Настроить профиль")
async def profile_handler(message: types.Message):
    logger.info("User pressed 'Настроить профиль'")
    # Логика обработки кнопки "Настроить профиль"
    await message.answer("Вы можете настроить свой профиль. Выберите параметры:")

    # Отправляем пользователю клавиатуру с настройками
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    profile_button_1 = KeyboardButton("Изменить пол")
    profile_button_2 = KeyboardButton("Изменить вид спорта")
    profile_button_3 = KeyboardButton("Изменить уровень нагрузки")
    keyboard.add(profile_button_1, profile_button_2, profile_button_3)

    await message.answer("Выберите, что хотите изменить:", reply_markup=keyboard)


# Обработчик кнопки "Изменить пол"
@dp.message_handler(lambda message: message.text == "Изменить пол")
async def change_gender(message: types.Message):
    logger.info("User pressed 'Изменить пол'")
    await message.answer("Пожалуйста, выберите свой пол:", reply_markup=gender_keyboard)


# Обработчик кнопки "Изменить вид спорта"
@dp.message_handler(lambda message: message.text == "Изменить вид спорта")
async def change_sport(message: types.Message):
    logger.info("User pressed 'Изменить вид спорта'")
    await message.answer("Пожалуйста, выберите вид спорта:", reply_markup=sport_keyboard)


# Обработчик кнопки "Изменить уровень нагрузки"
@dp.message_handler(lambda message: message.text == "Изменить уровень нагрузки")
async def change_intensity(message: types.Message):
    logger.info("User pressed 'Изменить уровень нагрузки'")
    await message.answer("Пожалуйста, выберите уровень нагрузки:", reply_markup=intensity_keyboard)


# Обработка ошибок
@dp.errors_handler()
async def error_handler(update, exception):
    logger.error(f"Exception occurred: {exception}")
    return True

# Запуск бота
if __name__ == "__main__":
    logger.info("Bot started")
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
