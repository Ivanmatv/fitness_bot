from aiogram import types
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import User, Workout, Exercise
import random
import json

REST_RECOMMENDATION = {
    "light": "Отдыхайте 60 секунд между подходами.",
    "medium": "Отдыхайте 90 секунд между подходами.",
    "heavy": "Отдыхайте 120+ секунд между подходами."
}

async def generate_workout(message: types.Message):
    user_id = message.from_user.id
    db: Session = SessionLocal()
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        await message.answer("Вы ещё не настроили профиль! Введите /start, чтобы начать.")
        db.close()
        return

    # Определяем спорт и уровень нагрузки
    sport_value = user.sport
    intensity_value = user.intensity

    # Ищем упражнения для выбранного вида спорта
    # Для этого предполагается, что sport в Exercise — это ForeignKey(sports.id),
    # и нужно сначала получить id соответствующего вида спорта.
    # Упрощённо:  
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
        db.close()
        return

    # Получаем последний Workout
    last_workout = db.query(Workout).filter(Workout.user_id == user_id).order_by(Workout.id.desc()).first()
    last_exercises = []
    if last_workout:
        try:
            last_exercises = json.loads(last_workout.exercises)
        except:
            # Если exercises хранилось в другом формате
            last_exercises = last_workout.exercises.split(",")

    # Фильтруем упражнения, чтобы не повторять упражнения из прошлого раза
    filtered_exercises = [ex for ex in exercises if ex.name not in last_exercises]

    if not filtered_exercises:
        # Если все упражнения совпали с предыдущей тренировкой, будем их повторять,
        # но предупреждать пользователя, что "свежих" нет
        await message.answer("Все упражнения совпадают с предыдущей тренировкой. Повторим тот же набор.")
        filtered_exercises = exercises
    
    # Генерируем список упражнений
    workout_exercises = generate_exercise_list(filtered_exercises, intensity_value)
    
    # Сохраняем тренировку в JSON-формате (пример)
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

    # Формируем текст ответа
    text_lines = []
    for ex in workout_exercises:
        line = f"• {ex.name}"
        if ex.image_url:
            line += f" (Изображение: {ex.image_url})"
        text_lines.append(line)

    workout_text = "\n".join(text_lines)
    reply_text = (
        f"💪 Ваша тренировка ({intensity_value}):\n\n"
        f"{workout_text}\n\n"
        f"Рекомендации по отдыху: {rest_advice}"
    )
    await message.answer(reply_text)

    # При желании можно отправлять изображения отдельно, если нужно
    for img in workout_ex_images:
        await message.answer_photo(img, caption="Вот изображение упражнения")

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
