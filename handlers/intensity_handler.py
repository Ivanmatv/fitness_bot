from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from states import WorkoutStates
from .workout_handler import generate_workout

router = Router(name="intensity_handler")


async def choose_intensity(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Лёгкий", callback_data="intensity_light"),
                InlineKeyboardButton(text="Средний", callback_data="intensity_medium"),
                InlineKeyboardButton(text="Тяжёлый", callback_data="intensity_heavy")
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data="intensity_back")
            ]
        ]
    )
    await message.answer("Выберите уровень нагрузки:", reply_markup=keyboard)

@router.callback_query(WorkoutStates.waiting_for_intensity, lambda c: c.data.startswith("intensity_"))
async def intensity_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    intensity_code = callback_query.data.split("_")[1]
    intensity_map = {"light": "light", "medium": "medium", "heavy": "heavy"}
    intensity_name_map = {"light": "Лёгкий", "medium": "Средний", "heavy": "Тяжёлый"}

    intensity = intensity_map.get(intensity_code)
    intensity_name = intensity_name_map.get(intensity_code)

    await state.update_data(intensity=intensity)
    await callback_query.answer(f"Уровень: {intensity_name}")
    await callback_query.message.edit_text(f"✅ Уровень нагрузки: {intensity_name}\n\nГенерирую тренировку...")

    # Получаем данные и генерируем тренировку
    data = await state.get_data()
    print(f"DEBUG: data from state = {data}")
    sport = data.get("sport")
    intensity = data.get("intensity")
    print(f"DEBUG: sport={sport}, intensity={intensity}")

    await generate_workout(
        user_id=callback_query.from_user.id,
        message=callback_query.message,
        sport=sport,
        intensity=intensity
    )
    await state.clear()
