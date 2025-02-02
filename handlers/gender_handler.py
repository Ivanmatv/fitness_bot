from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.database import SessionLocal
from db.models import User

async def set_gender(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="Мужчина", callback_data="gender_M"),
        InlineKeyboardButton(text="Женщина", callback_data="gender_F")
    )
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="gender_back"))
    await message.answer("Пожалуйста, выберите ваш пол:", reply_markup=keyboard)

async def gender_callback_handler(callback_query: types.CallbackQuery):
    db = SessionLocal()
    user_id = callback_query.from_user.id
    user = db.query(User).filter(User.id == user_id).first()

    data = callback_query.data.split("_")

    if len(data) < 2:
        # Обработка нажатия "Назад"
        await callback_query.answer("Возвращаемся назад")
        await callback_query.message.edit_text("Вы вернулись назад. Используйте /start для повторной настройки.")
        db.close()
        return

    key = data[1]

    if key == "M":
        gender_text = "Мужчина"
        if not user:
            user = User(id=user_id, gender='M', sport='fitness', intensity='light')
            db.add(user)
        else:
            user.gender = 'M'
        db.commit()
    elif key == "F":
        gender_text = "Женщина"
        if not user:
            user = User(id=user_id, gender='F', sport='fitness', intensity='light')
            db.add(user)
        else:
            user.gender = 'F'
        db.commit()
    else:
        gender_text = "Неизвестно"

    await callback_query.answer(f"Вы выбрали: {gender_text}", show_alert=True)
    await callback_query.message.edit_text(f"Пол установлен: {gender_text}")
    db.close()
