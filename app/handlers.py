from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter

from database import add_user, get_user, get_sport_id, add_workout, add_workout_exercise
from workout_generator import generate_workout
from datetime import datetime

from logger import get_logger

logger = get_logger()


# Состояния для FSM
class Form(StatesGroup):
    gender = State()
    sport = State()
    load_level = State()


# Общая строка меню
MENU_ROW = [KeyboardButton(text="/start"), KeyboardButton(text="/newworkout")]

# Клавиатура для выбора пола
gender_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="М"), KeyboardButton(text="Ж")]
    ],
    resize_keyboard=True
)

# Клавиатура для выбора вида спорта
sport_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="фитнес"), KeyboardButton(text="пауэрлифтинг")],
        [KeyboardButton(text="тяжёлая атлетика"), KeyboardButton(text="кроссфит")]
    ],
    resize_keyboard=True
)

# Клавиатура для выбора нагрузки
load_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="лёгкий"), KeyboardButton(text="средний"), KeyboardButton(text="тяжёлый")]
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
        await message.answer("Привет! Давай начнём с твоего пола (М/Ж):", reply_markup=with_menu(gender_kb))
        await state.set_state(Form.gender)
        logger.info(f"Установлено состояние Form.gender для пользователя {message.from_user.id}")


async def cmd_newworkout(message: types.Message, state: FSMContext):
    logger.info(f"/newworkout от пользователя {message.from_user.id}")
    await message.answer("Выбери пол (М/Ж):", reply_markup=with_menu(gender_kb))
    await state.set_state(Form.gender)
    logger.info(f"Установлено состояние Form.gender для пользователя {message.from_user.id} при /newworkout")


async def process_gender(message: types.Message, state: FSMContext):
    logger.info(f"process_gender: пользователь {message.from_user.id} ввёл {message.text}")
    if message.text not in ["М", "Ж"]:
        logger.warning(f"Пользователь {message.from_user.id} ввёл некорректный пол: {message.text}")
        await message.answer("Пожалуйста, выберите пол кнопками ниже.")
        return
    add_user(message.from_user.id, message.text)
    await message.answer("Выбери вид спорта:", reply_markup=with_menu(sport_kb))
    await state.set_state(Form.sport)


async def process_sport(message: types.Message, state: FSMContext):
    logger.info(f"process_sport: пользователь {message.from_user.id} ввёл {message.text}")
    sports = ["фитнес", "пауэрлифтинг", "тяжёлая атлетика", "кроссфит"]
    if message.text not in sports:
        logger.warning(f"Пользователь {message.from_user.id} ввёл некорректный спорт: {message.text}")
        await message.answer("Пожалуйста, выбери вид спорта кнопками.")
        return
    await state.update_data(sport=message.text)
    await message.answer("Выбери уровень нагрузки на тренировке:", reply_markup=with_menu(load_kb))
    await state.set_state(Form.load_level)
    logger.info(f"Пользователь {message.from_user.id} выбрал спорт {message.text}, состояние Form.load_level")


async def process_load_level(message: types.Message, state: FSMContext):
    logger.info(f"process_load_level: пользователь {message.from_user.id} ввёл {message.text}")
    load_levels = ["лёгкий", "средний", "тяжёлый"]
    if message.text not in load_levels:
        logger.warning(f"Пользователь {message.from_user.id} ввёл некорректный уровень нагрузки: {message.text}")
        await message.answer("Пожалуйста, выбери уровень нагрузки кнопками.")
        return
    data = await state.get_data()
    sport_name = data['sport']

    user = get_user(message.from_user.id)
    if not user:
        logger.error(f"Пользователь {message.from_user.id} не найден в базе при выборе нагрузки")
        await message.answer("Произошла ошибка, попробуйте начать заново /start")
        await state.finish()
        return

    sport_id = get_sport_id(sport_name)
    workout = generate_workout(user['id'], sport_id, message.text)

    # Запись тренировки в БД
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    workout_id = add_workout(user['id'], sport_id, message.text, date_str)
    for ex in workout:
        add_workout_exercise(workout_id, ex['id'])

    # Формируем сообщение с упражнениями
    text = "Твоя тренировка:\n\n"
    for i, ex in enumerate(workout, 1):
        text += f"{i}. {ex['name']} — {ex['description']}\nПовторений: {ex.get('repetitions', 'N/A')}\n\n"

    await message.answer(text)
    logger.info(f"Пользователь {message.from_user.id} получил тренировку: спорт={sport_name}, нагрузка={message.text}")
    await state.clear()


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command(commands=["start"]))
    dp.message.register(cmd_newworkout, Command(commands=["newworkout"]))
    dp.message.register(process_gender, StateFilter(Form.gender))
    dp.message.register(process_sport, StateFilter(Form.sport))
    dp.message.register(process_load_level, StateFilter(Form.load_level))
