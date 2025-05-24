import random
from database import (
    get_exercises_for_sport_and_load,
    get_last_workout_exercises
)


def generate_workout(user_id, sport_id, load_level):
    all_exercises = get_exercises_for_sport_and_load(sport_id, load_level)
    last_exercise_ids = get_last_workout_exercises(user_id)

    # Фильтруем упражнения, которые были на последней тренировке
    filtered_exercises = [
        ex for ex in all_exercises if ex['id'] not in last_exercise_ids
    ]

    # Если после фильтрации мало упражнений, берём все (чтобы не было пусто)
    if len(filtered_exercises) < 3:
        filtered_exercises = all_exercises

    # Выбираем случайно 5 упражнений для тренировки
    workout = random.sample(filtered_exercises, min(5, len(filtered_exercises)))

    return workout
