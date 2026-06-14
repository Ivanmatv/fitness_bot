from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from .intensity_handler import choose_intensity
from states import WorkoutStates


router = Router(name="sport_handler")

@router.message(lambda msg: msg.text == "Получить тренировку")
async def choose_sport(message: types.Message, state: FSMContext):
    await state.set_state(WorkoutStates.waiting_for_sport)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Фитнес", callback_data="sport_fitness"),
                InlineKeyboardButton(text="Пауэрлифтинг", callback_data="sport_powerlifting")
            ],
            [
                InlineKeyboardButton(text="Кроссфит", callback_data="sport_crossfit"),
                InlineKeyboardButton(text="Тяжёлая атлетика", callback_data="sport_weightlifting")
            ]
        ]
    )
    await message.answer("Выберите вид спорта для тренировки:", reply_markup=keyboard)

@router.callback_query(WorkoutStates.waiting_for_sport, lambda c: c.data.startswith("sport_"))
async def sport_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    sport_code = callback_query.data.split("_")[1]
    sport_map = {
        "fitness": "fitness",
        "powerlifting": "powerlifting",
        "crossfit": "crossfit",
        "weightlifting": "weightlifting"
    }
    sport_name_map = {
        "fitness": "Фитнес",
        "powerlifting": "Пауэрлифтинг",
        "crossfit": "Кроссфит",
        "weightlifting": "Тяжёлая атлетика"
    }

    sport = sport_map.get(sport_code)
    sport_name = sport_name_map.get(sport_code)

    await state.update_data(sport=sport)
    await callback_query.answer(f"Выбрано: {sport_name}")
    await callback_query.message.edit_text(f"✅ Вид спорта: {sport_name}\n\nТеперь выберите уровень нагрузки:")

    # Переходим к выбору интенсивности
    await state.set_state(WorkoutStates.waiting_for_intensity)
    await choose_intensity(callback_query.message, state)
