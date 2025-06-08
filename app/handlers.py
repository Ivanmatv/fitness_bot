import json

from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from datetime import datetime

from database import add_user, get_user, get_sport_id, add_workout, add_workout_exercise, get_workout_history
from workout_generator import generate_workout
from logger import get_logger

logger = get_logger()


# Состояния для FSM
class Form(StatesGroup):
    sport = State()
    workout_type = State()
    split_type = State()
    load_level = State()


# Общая строка меню
MENU_ROW = [
    KeyboardButton(text="/start"),
    KeyboardButton(text="/newworkout"),
    KeyboardButton(text="/history")
]

# Клавиатура для выбора вида спорта
sport_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="фитнес"), KeyboardButton(text="пауэрлифтинг")],
        [KeyboardButton(text="тяжёлая атлетика"), KeyboardButton(text="кроссфит")]
    ],
    resize_keyboard=True
)

# Клавиатура для выбора типа тренировки (фитнес)
fitness_type_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Всё тело"), KeyboardButton(text="Сплит-тренировка")]
    ],
    resize_keyboard=True
)

# Клавиатура для выбора типа сплит-тренировки
fitness_split_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Грудь + руки")],
        [KeyboardButton(text="Спина + руки")],
        [KeyboardButton(text="Ноги + плечи")]
    ],
    resize_keyboard=True
)

# Клавиатура для выбора типа тренировки (пауэрлифтинг)
pl_type_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Жимовая + ноги")],
        [KeyboardButton(text="Тяговая + спина")],
        [KeyboardButton(text="Ноги + жимовая")]
    ],
    resize_keyboard=True
)

# Клавиатура для выбора типа тренировки (тяжёлая атлетика)
ta_type_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Рывковая")],
        [KeyboardButton(text="Толчковая")]
    ],
    resize_keyboard=True
)

# Клавиатура для выбора нагрузки
load_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="лёгкий")],
        [KeyboardButton(text="средний")],
        [KeyboardButton(text="тяжёлый")]
    ],
    resize_keyboard=True
)


def with_menu(base_kb: ReplyKeyboardMarkup) -> ReplyKeyboardMarkup:
    """Возвращает копию базовой клавиатуры с добавленной внизу строкой MENU_ROW"""
    # Клонируем объект
    kb = ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True)
    # Копируем существующие ряды кнопок
    for row in base_kb.keyboard:
        kb.keyboard.append(list(row))
    # Добавляем строку меню
    kb.keyboard.append(list(MENU_ROW))
    return kb


async def cmd_start(message: types.Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} начал работу с ботом")
    user = get_user(message.from_user.id)
    if user:
        await message.answer("С возвращением! Хотите новую тренировку? Введите /newworkout")
    else:
        # Регистрация пользователя
        add_user(message.from_user.id, None)
        await message.answer("Привет! Выбери вид спорта:", reply_markup=with_menu(sport_kb))
        await state.set_state(Form.sport)
        logger.info(f"Установлено состояние Form.sport для пользователя {message.from_user.id}")


async def cmd_newworkout(message: types.Message, state: FSMContext):
    logger.info(f"/newworkout от пользователя {message.from_user.id}")
    await message.answer("Выбери вид спорта:", reply_markup=with_menu(sport_kb))
    await state.set_state(Form.sport)
    logger.info(f"Установлено состояние Form.sport для пользователя {message.from_user.id} при /newworkout")


async def process_sport(message: types.Message, state: FSMContext):
    logger.info(f"process_sport: пользователь {message.from_user.id} ввёл {message.text}")
    sports = ["фитнес", "пауэрлифтинг", "тяжёлая атлетика", "кроссфит"]
    if message.text not in sports:
        logger.warning(f"Пользователь {message.from_user.id} ввёл некорректный спорт: {message.text}")
        await message.answer("Пожалуйста, выбери вид спорта кнопками.")
        return
    await state.update_data(sport=message.text)
    if message.text == "фитнес":
        await message.answer("Выбери тип тренировки:", reply_markup=with_menu(fitness_type_kb))
        await state.set_state(Form.workout_type)
    elif message.text == "пауэрлифтинг":
        await message.answer("Выбери тип тренировки:", reply_markup=with_menu(pl_type_kb))
        await state.set_state(Form.workout_type)
    elif message.text == "тяжёлая атлетика":
        await message.answer("Выбери тип тренировки:", reply_markup=with_menu(ta_type_kb))
        await state.set_state(Form.workout_type)
    elif message.text == "кроссфит":
        await message.answer("Выбери тип тренировки:", reply_markup=with_menu(load_kb))
        await state.set_state(Form.load_level)


async def process_fitness_type(message: types.Message, state: FSMContext):
    logger.info(f"process_fitness_type: пользователь {message.from_user.id} ввёл {message.text}")
    t = message.text
    if t == "Всё тело":
        await state.update_data(workout_type="Всё тело")
        await message.answer("Выбери уровень нагрузки:", reply_markup=with_menu(load_kb))
        await state.set_state(Form.load_level)
    elif t == "Сплит-тренировка":
        await state.update_data(workout_type="Сплит-тренировка")
        await message.answer("Выбери уровень нагрузки:", reply_markup=with_menu(fitness_split_kb))
        await state.set_state(Form.split_type)
    else:
        await message.answer("Пожалуйста, выберити тип тренировки.")


async def process_fitness_split_type(message: types.Message, state: FSMContext):
    logger.info(f"process_fitness_type: пользователь {message.from_user.id} ввёл {message.text}")
    split = message.text
    splits = ["Грудь + руки", "Спина + руки", "Ноги + плечи"]
    if split not in splits:
        await message.answer("Пожалуйста, выберити вариант из предложенных.")
        return
    await state.update_data(split_type=split)
    await message.answer("Выбери уровень нагрузки:", reply_markup=with_menu(load_kb))
    await state.set_state(Form.load_level)


async def process_pl_type(message: types.Message, state: FSMContext):
    logger.info(f"process_fitness_type: пользователь {message.from_user.id} ввёл {message.text}")
    pl_types = ["Жимовая + ноги", "Тяговая + спина", "Ноги + жимовая"]
    if message.text not in pl_types:
        await message.answer("Пожалуйста, выбери тип тренировки.")
        return
    await state.update_data(workout_type=message.text)
    await message.answer("Выбери уровень нагрузки:", reply_markup=with_menu(load_kb))
    await state.set_state(Form.load_level)


async def process_ta_type(message: types.Message, state: FSMContext):
    logger.info(f"process_fitness_type: пользователь {message.from_user.id} ввёл {message.text}")
    ta_types = ["Рывковая", "Толчковая"]
    if message.text not in ta_types:
        await message.answer("Пожалуйста, выбери тип тренировки.")
        return
    await state.update_data(workout_type=message.text)
    await message.answer("Выбери уровень нагрузки:", reply_markup=with_menu(load_kb))
    await state.set_state(Form.load_level)


async def process_load_level(message: types.Message, state: FSMContext):
    logger.info(f"process_load_level: пользователь {message.from_user.id} ввёл {message.text}")
    load_levels = ["лёгкий", "средний", "тяжёлый"]
    if message.text not in load_levels:
        logger.warning(f"Пользователь {message.from_user.id} ввёл некорректный уровень нагрузки: {message.text}")
        await message.answer("Пожалуйста, выбери уровень нагрузки кнопками.")
        return
    data = await state.get_data()
    sport_name = data.get('sport')
    workout_type = data.get('workout_type')
    split_type = data.get('split_type')
    load_level = message.text

    user = get_user(message.from_user.id)
    if not user:
        logger.error(f"Пользователь {message.from_user.id} не найден в базе при выборе нагрузки")
        await message.answer("Произошла ошибка, попробуйте начать заново /start")
        await state.finish()
        return

    sport_id = get_sport_id(sport_name)
    workout = generate_workout(
        user['id'], sport_id, load_level,
        workout_type=workout_type,
        split_type=split_type
    )

    logger.info(
        f"Сформирована тренировка для пользователя {user['id']}:\n" +
        json.dumps([
            {
                "name": ex['name'],
                "description": ex.get('description', ''),
                "repetitions": ex.get('repetitions', 'N/A')
            } for ex in workout
        ], ensure_ascii=False, indent=2)
    )

    # Запись тренировки в БД
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    workout_id = add_workout(user['id'], sport_id, load_level, date_str)
    for ex in workout:
        add_workout_exercise(workout_id, ex['id'])

    # Формируем сообщение с упражнениями
    text = "Твоя тренировка:\n\n"
    for i, ex in enumerate(workout, 1):
        text += f"{i}. {ex['name']} — {ex['description']}\nПовторений: {ex.get('repetitions', 'N/A')}\n\n"

    await message.answer(text)
    logger.info(f"Пользователь {message.from_user.id} получил тренировку: спорт={sport_name}, нагрузка={message.text}")
    await state.clear()


async def cmd_history(message: types.Message):
    user = get_user(message.from_user.id)
    if not user:
        await message.answer("Сначала запустите бота: /start")
        return

    history = get_workout_history(user['id'])
    if not history:
        await message.answer("Пока нет ни одной завершённой тренировки.", reply_markup=with_menu(MENU_ROW))
        return

    # Формируем текст
    for w in history:
        text = (
            f"📅 {w['date']}\n"
            f"🏋️ Вид спорта: {w['sport']}\n"
            f"💪 Нагрузка: {w['load']}\n\n"
            "Упражнения:\n"
        )
        for i, ex in enumerate(w['exercises'], 1):
            text += f"{i}. {ex['name']} — {ex['description']} ({ex['repetitions']} повт.)\n"
        await message.answer(text, reply_markup=with_menu(sport_kb))


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command(commands=["start"]))
    dp.message.register(cmd_newworkout, Command(commands=["newworkout"]))
    dp.message.register(cmd_history, Command(commands=["history"]))
    dp.message.register(process_sport, StateFilter(Form.sport))
    dp.message.register(process_load_level, StateFilter(Form.load_level))
    dp.message.register(process_fitness_type, StateFilter(Form.workout_type), is_fitness)
    dp.message.register(process_fitness_split_type, StateFilter(Form.split_type))
    dp.message.register(process_pl_type, StateFilter(Form.workout_type), is_powerlifting)
    dp.message.register(process_ta_type, StateFilter(Form.workout_type), is_weightlifting)


async def is_fitness(msg: types.Message, state: FSMContext) -> bool:
    data = await state.get_data()
    return data.get('sport') == "фитнес"


async def is_powerlifting(msg: types.Message, state: FSMContext) -> bool:
    data = await state.get_data()
    return data.get('sport') == "пауэрлифтинг"


async def is_weightlifting(msg: types.Message, state: FSMContext) -> bool:
    data = await state.get_data()
    return data.get('sport') == "тяжёлая атлетика"
