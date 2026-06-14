import random
import logging

from aiogram import types

from db.database import SessionLocal
from db.models import User, Workout, Exercise, WorkoutExercise

REST_RECOMMENDATION = {
    "light": "Отдыхайте 60 секунд между подходами.",
    "medium": "Отдыхайте 90 секунд между подходами.",
    "heavy": "Отдыхайте 120+ секунд между подходами."
}

# Маппинг названий видов спорта в их ID (должны соответствовать данным в БД)
SPORT_ID_MAP = {
    "fitness": 1,
    "powerlifting": 2,
    "crossfit": 3,
    "weightlifting": 4
}

# Маппинг уровня интенсивности в ID (зависит от записей в таблице intensity_levels)
INTENSITY_ID_MAP = {
    "light": 1,
    "medium": 2,
    "heavy": 3
}

# Количество подходов в зависимости от интенсивности
SETS_COUNT = {
    "light": 2,
    "medium": 3,
    "heavy": 4
}


async def generate_workout(message: types.Message, sport=None, intensity=None):
    """Генерация тренировки с возможностью передачи sport и intensity (строковые названия)"""
    print(f"DEBUG: generate_workout called with sport={sport}, intensity={intensity}")
    user_id = message.from_user.id
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.id == user_id).first()
        print(f"DEBUG: user found = {user is not None}")
        if not user:
            await message.answer(
                "Вы ещё не настроили профиль! Нажмите кнопку «Настроить профиль»."
            )
            return

        # Получаем последнюю тренировку пользователя
        last_workout = db.query(Workout).filter(Workout.user_id == user_id) \
            .order_by(Workout.id.desc()).first()

        # Если вид спорта не передан явно – берём из последней тренировки
        if not sport:
            if last_workout:
                sport = last_workout.sport.name   # через relationship
            else:
                sport = "fitness"

        # Если интенсивность не передана – берём из последней тренировки
        if not intensity:
            if last_workout:
                intensity = last_workout.intensity.name
            else:
                intensity = "medium"

        # Получаем ID спорта
        sport_id = SPORT_ID_MAP.get(sport)
        if sport_id is None:
            await message.answer("Неизвестный вид спорта. Попробуйте другой.")
            return

        # Получаем ID интенсивности
        intensity_id = INTENSITY_ID_MAP.get(intensity)
        if intensity_id is None:
            await message.answer("Неизвестный уровень нагрузки. Попробуйте другой.")
            return

        # Загружаем все упражнения для выбранного вида спорта
        exercises = db.query(Exercise).filter(Exercise.sport_id == sport_id).all()
        print(f"DEBUG: found {len(exercises)} exercises for sport_id={sport_id}")
        if not exercises:
            await message.answer("В базе данных пока нет упражнений для этого вида спорта.")
            return

        # ID упражнений из последней тренировки (чтобы избежать повторений)
        last_exercise_ids = []
        if last_workout:
            last_exercise_ids = [
                we.exercise_id
                for we in db.query(WorkoutExercise)
                .filter(WorkoutExercise.workout_id == last_workout.id).all()
            ]

        # Исключаем упражнения, которые были в прошлый раз
        filtered_exercises = [ex for ex in exercises if ex.id not in last_exercise_ids]
        if not filtered_exercises:
            await message.answer(
                "Все упражнения совпадают с предыдущей тренировкой. Повторяем набор."
            )
            filtered_exercises = exercises

        # Генерируем список упражнений для тренировки
        workout_exercises = generate_exercise_list(filtered_exercises, intensity)

        # Рекомендация по отдыху
        rest_advice = REST_RECOMMENDATION.get(
            intensity, "Отдыхайте 60–90 секунд между подходами."
        )

        # Создаём новую тренировку в БД
        new_workout = Workout(
            user_id=user_id,
            sport_id=sport_id,
            intensity_id=intensity_id,
            rest_recommendation=rest_advice
        )
        db.add(new_workout)
        db.commit()
        db.refresh(new_workout)

        # Количество подходов для текущей интенсивности
        sets = SETS_COUNT.get(intensity, 3)

        # Добавляем упражнения в связующую таблицу
        for order, exercise in enumerate(workout_exercises, start=1):
            workout_ex = WorkoutExercise(
                workout_id=new_workout.id,
                exercise_id=exercise.id,
                exercise_order=order,
                exercise_count=sets          # одинаковое число подходов для всех упражнений
            )
            db.add(workout_ex)
        db.commit()

        # Формируем текст для ответа пользователю
        text_lines = [f"• {exercise.name}" for exercise in workout_exercises]
        joined_lines = '\n'.join(text_lines)
        reply_text = (
            f"Ваша тренировка\n"
            f"Вид спорта: {sport}\n"
            f"Уровень: {intensity}\n"
            f"{joined_lines}\n\n"
            f"Количество подходов: {sets}\n"
            f"Рекомендации по отдыху: {rest_advice}"
        )

        await message.answer(reply_text, parse_mode="Markdown")

        # Отправляем фото для каждого упражнения (если есть)
        for exercise in workout_exercises:
            if exercise.image_url:
                await message.answer_photo(exercise.image_url, caption=exercise.name)

    except Exception as e:
        print(f"DEBUG: EXCEPTION: {e}")
        logging.error(f"Ошибка в generate_workout: {e}", exc_info=True)
        await message.answer("Произошла ошибка. Попробуйте ещё раз.")
    finally:
        db.close()


def generate_exercise_list(exercises, intensity):
    """Возвращает случайный набор упражнений в зависимости от интенсивности"""
    exercise_count = {
        "light": 3,
        "medium": 5,
        "heavy": 7
    }.get(intensity, 5)

    if len(exercises) <= exercise_count:
        return exercises
    else:
        return random.sample(exercises, exercise_count)