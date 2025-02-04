# intensity_handler.py
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.database import SessionLocal
from db.models import User
from logger import get_logger

logger = get_logger()

INTENSITY_INFO = {
    "light": "Лёгкий уровень нагрузки: 2–3 упражнения на группу мышц, короткие подходы и больше отдыха.",
    "medium": "Средний уровень нагрузки: 4–5 упражнений, умеренные веса, отдых 60–90 секунд.",
    "heavy": "Тяжёлый уровень нагрузки: 6–7 упражнений, большие веса, отдых 2–3 минуты."
}

async def set_intensity(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Лёгкий", callback_data="intensity_light"),
        InlineKeyboardButton(text="Средний", callback_data="intensity_medium"),
        InlineKeyboardButton(text="Тяжёлый", callback_data="intensity_heavy"),
        InlineKeyboardButton(text="Назад", callback_data="intensity_back")
    )
    await message.answer("Выберите уровень нагрузки для тренировки:", reply_markup=keyboard)

async def intensity_callback_handler(callback_query: types.CallbackQuery):
    db = SessionLocal()
    try:
        user_id = callback_query.from_user.id
        user = db.query(User).filter(User.id == user_id).first()

        data = callback_query.data.split("_")
        if len(data) < 2:
            await callback_query.answer("Возвращаемся назад")
            await callback_query.message.edit_text("Вы вернулись назад. Используйте /start для повторной настройки.")
            return

        code = data[1]

        if not user:
            user = User(id=user_id, gender='M', sport='fitness', intensity='light')
            db.add(user)
            db.commit()

        intensity_map = {"light": "light", "medium": "medium", "heavy": "heavy"}
        user.intensity = intensity_map.get(code, "light")
        db.commit()

        info = INTENSITY_INFO.get(code, "")
        await callback_query.answer(f"Установлен уровень: {info}", show_alert=True)
        await callback_query.message.edit_text(f"Уровень нагрузки: {info}")
    except Exception as e:
        logger.error(f"Error in intensity_callback_handler: {e}")
        await callback_query.answer("Произошла ошибка. Попробуйте ещё раз.")
    finally:
        db.close()