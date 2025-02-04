# workout_handler.py
from aiogram import types
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import User, Workout, Exercise
import random
import json
from logger import get_logger

logger = get_logger()

REST_RECOMMENDATION = {
    "light": "Отдыхайте 60 секунд между подходами.",
    "medium": "Отдыхайте 90 секунд между подходами.",
    "heavy": "Отдыхайте 120+ секунд между подходами."
}

async def generate_workout(message: types.Message):
    user_id = message.from_user.id
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            await message.answer("Вы ещё не настроили профиль! Введите /start, чтобы начать.")
            return

        sport_value = user.sport
        intensity_value = user.intensity

        sport_id_map = {
            "fitness": 1,
            "powerlifting": 2,
            "crossfit": 3,
            "weightlifting": 4
        }
        sport_id = sport_id_map.get(sport_value, 1)
        
        exercises = db.query(Exercise).filter(Exercise.sport_id == sport_id).all()
        if not exercises:
            await message.answer("В базе данных нет упражнений для выбранного вида спорта.")
            return

        last_workout = db.query(Workout).filter(Workout.user_id == user_id).order_by(Workout.id.desc()).first()
        last_exercises = []
        if last_workout:
            try:
                last_exercises = json.loads(last_workout.exercises)
            except:
                last_exercises = last_workout.exercises.split(",")

        filtered_exercises = [ex for ex in exercises if ex.name not in last_exercises]
        if not filtered_exercises:
            await message.answer("Все упражнения совпадают с предыдущей тренировкой. Повторим тот же набор.")
            filtered_exercises = exercises
        
        workout_exercises = generate_exercise_list(filtered_exercises, intensity_value)
        workout_ex_names = [ex.name for ex in workout_exercises]
        workout_ex_images = [ex.image_url for ex in workout_exercises if ex.image_url]

        workout_data = json.dumps(workout_ex_names, ensure_ascii=False)
        rest_advice = REST_RECOMMENDATION.get(intensity_value, "Отдыхайте 60–90 секунд между подходами.")
        
        new_workout = Workout(
            user_id=user_id,
            exercises=workout_data,
            rest_recommendation=rest_advice
        )
        db.add(new_workout)
        db.commit()

        text_lines = [f"• {ex.name}" for ex in workout_exercises]
        workout_text = "\n".join(text_lines)
        reply_text = (
            f"💪 Ваша тренировка ({intensity_value}):\n\n"
            f"{workout_text}\n\n"
            f"Рекомендации по отдыху: {rest_advice}"
        )
        await message.answer(reply_text)

        for img in workout_ex_images:
            await message.answer_photo(img, caption="Вот изображение упражнения")
    except Exception as e:
        logger.error(f"Error in generate_workout: {e}")
        await message.answer("Произошла ошибка при генерации тренировки. Попробуйте ещё раз.")
    finally:
        db.close()

def generate_exercise_list(exercises, intensity):
    exercise_count = {
        "light": 3,
        "medium": 5,
        "heavy": 7
    }.get(intensity, 3)

    if len(exercises) < exercise_count:
        # Если упражнений меньше, чем нужно, берём все
        selected = exercises
    else:
        selected = random.sample(exercises, exercise_count)

    return selected
