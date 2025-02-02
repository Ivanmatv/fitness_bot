from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.database import SessionLocal
from db.models import User

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
    user_id = callback_query.from_user.id
    user = db.query(User).filter(User.id == user_id).first()

    data = callback_query.data.split("_")

    if len(data) < 2:
        # Обработка кнопки "Назад"
        await callback_query.answer("Возвращаемся назад")
        await callback_query.message.edit_text("Вы вернулись назад. Используйте /start для повторной настройки.")
        db.close()
        return

    sport_code = data[1]
    sport_mapping = {
        "fitness": "fitness",
        "powerlifting": "powerlifting",
        "crossfit": "crossfit",
        "weightlifting": "weightlifting"
    }

    if not user:
        user = User(id=user_id, gender='M', sport='fitness', intensity='light')
        db.add(user)
        db.commit()

    user.sport = sport_mapping.get(sport_code, "fitness")
    db.commit()

    sport_name = {
        "fitness": "Фитнес",
        "powerlifting": "Пауэрлифтинг",
        "crossfit": "Кроссфит",
        "weightlifting": "Тяжёлая атлетика"
    }.get(sport_code, "Фитнес")

    await callback_query.answer(f"Вы выбрали: {sport_name}", show_alert=True)
    await callback_query.message.edit_text(f"Вид спорта установлен: {sport_name}")
    db.close()
