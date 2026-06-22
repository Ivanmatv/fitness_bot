import logging

from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.models import User
from db.database import SessionLocal
from handlers.start_handler import start_command

import sys
print("gender_handler загружен", file=sys.stderr)


logger = logging.getLogger(__name__)
router = Router(name="gender_handler")

@router.message(lambda msg: msg.text == "Настроить профиль")
async def set_gender(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Мужчина", callback_data="gender_M"),
                InlineKeyboardButton(text="Женщина", callback_data="gender_F")
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data="gender_back")
            ]
        ]
    )
    await message.answer("Пожалуйста, выберите ваш пол:", reply_markup=keyboard)
    print("Клавиатура отправлена", file=sys.stderr)

@router.callback_query(lambda c: c.data.startswith("gender_"))
async def gender_callback_handler(callback_query: types.CallbackQuery):
    print(f"Колбэк получен: {callback_query.data}", file=sys.stderr)
    print(f"🔥 CALLBACK ПРИШЁЛ: {callback_query.data} от пользователя {callback_query.from_user.id}")
    logging.info(f"CALLBACK: {callback_query.data}")
    db = SessionLocal()

    try:
        user_id = callback_query.from_user.id
        user = db.query(User).filter(User.id == user_id).first()

        data = callback_query.data.split("_")
        if len(data) < 2 or data[1] == "back":
            await callback_query.answer("Возвращаемся назад")
            await callback_query.message.edit_text(
                "Вы вернулись назад. "
                "Используйте /start для повторной настройки."
            )
            return

        gender_type = 1
        gender = data[gender_type]

        if not user:
            user = User(id=user_id, gender=gender)
            db.add(user)
        else:
            user.gender = gender

        db.commit()

        gender_text = "Мужчина" if gender == "M" else "Женщина"

        await callback_query.answer(f"Вы выбрали: {gender_text}", show_alert=True)
        logger.info(gender_text)
        await callback_query.message.edit_text(f"Пол установлен: {gender_text}")
        await start_command(callback_query.message)
    except Exception as e:
        logger.error(
            "Ошибка в gender_callback_handler для user "
            f"{callback_query.from_user.id}: {e}",
            exc_info=True
        )
        await callback_query.answer(
            "Произошла техническая ошибка. "
            "Попробуйте позже или начните заново через /start",
            show_alert=True
        )
        await callback_query.message.edit_text(
            "Ошибка. Используйте /start для повторной настройки."
        )
    finally:
        db.close()
