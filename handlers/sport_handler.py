# sport_handler.py
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.database import SessionLocal
from db.models import User
from logger import get_logger

logger = get_logger()

SPORT_MAPPING = {
    "fitness": "Фитнес",
    "powerlifting": "Пауэрлифтинг",
    "crossfit": "Кроссфит",
    "weightlifting": "Тяжёлая атлетика"
}

async def set_sport(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="Фитнес", callback_data="sport_fitness"),
        InlineKeyboardButton(text="Пауэрлифтинг", callback_data="sport_powerlifting"),
        InlineKeyboardButton(text="Кроссфит", callback_data="sport_crossfit"),
        InlineKeyboardButton(text="Тяжёлая атлетика", callback_data="sport_weightlifting"),
        InlineKeyboardButton(text="Назад", callback_data="sport_back")
    )
    await message.answer("Выберите ваш вид спорта:", reply_markup=keyboard)

async def sport_callback_handler(callback_query: types.CallbackQuery):
    db = SessionLocal()
    try:
        user_id = callback_query.from_user.id
        user = db.query(User).filter(User.id == user_id).first()

        data = callback_query.data.split("_")
        if len(data) < 2:
            await callback_query.answer("Возвращаемся назад")
            await callback_query.message.edit_text("Вы вернулись назад. Используйте /start для повторной настройки.")
            return

        sport_code = data[1]
        sport_name = SPORT_MAPPING.get(sport_code, "Фитнес")

        if not user:
            user = User(id=user_id, gender='M', sport='fitness', intensity='light')
            db.add(user)
            db.commit()

        user.sport = sport_code
        db.commit()

        await callback_query.answer(f"Вы выбрали: {sport_name}", show_alert=True)
        await callback_query.message.edit_text(f"Вид спорта установлен: {sport_name}")
    except Exception as e:
        logger.error(f"Error in sport_callback_handler: {e}")
        await callback_query.answer("Произошла ошибка. Попробуйте ещё раз.")
    finally:
        db.close()
