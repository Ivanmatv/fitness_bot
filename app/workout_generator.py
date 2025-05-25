import random
from database import (
    get_exercises_for_sport_and_load,
    get_last_workout_exercises
)


def generate_workout(user_id, sport_id, load_level):
    rows = get_exercises_for_sport_and_load(sport_id, load_level)
    last_ids = set(get_last_workout_exercises(user_id))

    # Фильтруем по ID, убираем последний комплекс
    pool = [r for r in rows if r['id'] not in last_ids]
    if len(pool) < 3:
        pool = rows

    # Берём 5 случайных
    picked = random.sample(pool, min(5, len(pool)))
    workout = []
    for row in picked:
        ex = dict(row)

        if load_level == 'лёгки':
            ex['repetitions'] = ex['reps_light']
        elif load_level == 'средний':
            ex['repetitions'] = ex['reps_medium']
        else:
            ex['repetitions'] = ex['reps_heavy']

        workout.append(ex)

    return workout
