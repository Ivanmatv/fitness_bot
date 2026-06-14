import random
from database import (
    get_sport_id,
    get_group_id,
    get_exercises_for_sport,
    get_last_workout_exercises,
    get_exercises_by_group
)


def is_similar_exercise(existing_exercises, new_exercise):
        """
        Проверяет, является ли новое упражнение слишком похожим на уже выбранные.
        """
        # Группы ключевых слов для похожих упражнений
        similar_keywords = {
            'Тяга становая': ['Тяга становая']
        }

        new_name = new_exercise['name']
        for keyword_group in similar_keywords.values():
            # Проверяем, содержит ли название нового упражнения ключевое слово из группы
            if any(keyword in new_name for keyword in keyword_group):
                for ex in existing_exercises:
                    if any(keyword in ex['name'] for keyword in keyword_group):
                        return True
        return False


def generate_workout(
    user_id, sport_id, load_level, workout_type=None, split_type=None
):
    """
    Формирует тренировку по выбранному виду спорта, типу и нагрузке.
    """
    # Собираем id упражнений из прошлой тренировки (чтобы не дублировать)
    last_ids = set(get_last_workout_exercises(user_id))
    workout = []

    # 1. ФИТНЕС
    if sport_id == get_sport_id("фитнес"):
        # Fullbody: ноги, спина, грудь, руки
        if workout_type == "Fullbody":
            groups = ["ноги", "спина", "грудь", "руки"]
        # Сплит-тренировки
        elif workout_type == "split":
            if split_type == "Грудь + руки":
                groups = ["грудь", "руки"]
            elif split_type == "Спина + руки":
                groups = ["спина", "руки"]
            elif split_type == "Ноги + плечи":
                groups = ["ноги", "плечи"]
            else:
                groups = ["ноги", "спина", "грудь", "руки"]  # fallback
        else:
            groups = ["ноги", "спина", "грудь", "руки"]  # fallback

        for group in groups:
            group_id = get_group_id(sport_id, group)
            exercises = get_exercises_by_group(group_id)
            pool = [ex for ex in exercises if ex["id"] not in last_ids]
            if not pool:
                pool = exercises
            if pool:
                # Фильтрация похожих упражнений
                filtered_pool = [
                    ex for ex in pool
                    if not is_similar_exercise(workout, ex)
                ]
                if not filtered_pool:
                    filtered_pool = pool
                ex = random.choice(filtered_pool)
                ex = dict(ex)
                ex["repetitions"] = select_reps(ex, load_level)
                workout.append(ex)
                last_ids.add(ex["id"])
        return workout

    # 2. ПАУЭРЛИФТИНГ
    if sport_id == get_sport_id("пауэрлифтинг"):
        # Шаблоны для типов тренировок
        pl_schemes = {
            "Жимовая + ноги": [
                ("жимовые упражнения", 2),
                ("ноги", 2)
            ],
            "Тяговая + спина": [
                ("тяговые упражнения", 2),
                ("спина", 2)
            ],
            "Ноги + жимовая": [
                ("ноги", 2),
                ("жимовые упражнения", 2)
            ]
        }
        scheme = pl_schemes.get(workout_type, [("жимовые упражнения", 2), ("ноги", 2)])
        for group, cnt in scheme:
            group_id = get_group_id(sport_id, group)
            exercises = get_exercises_by_group(group_id)
            pool = [ex for ex in exercises if ex["id"] not in last_ids]
            if len(pool) < cnt:
                pool = exercises
            # Фильтрация похожих упражнений
            filtered_pool = [
                ex for ex in pool
                if not is_similar_exercise(workout, ex)
            ]
            if len(filtered_pool) < cnt:
                filtered_pool = pool
            picked = random.sample(filtered_pool, min(cnt, len(pool)))
            for ex in picked:
                ex = dict(ex)
                ex["repetitions"] = select_reps(ex, load_level)
                workout.append(ex)
                last_ids.add(ex["id"])
        return workout

    # 3. ТЯЖЁЛАЯ АТЛЕТИКА
    if sport_id == get_sport_id("тяжёлая атлетика"):
        ta_types = {
            "Рывковая": ("рывковые упражнения", 3),
            "Толчковая": ("толчковые упражнения", 3)
        }
        group, cnt = ta_types.get(workout_type, ("рывковые упражнения", 3))
        group_id = get_group_id(sport_id, group)
        exercises = get_exercises_by_group(group_id)
        pool = [ex for ex in exercises if ex["id"] not in last_ids]
        if len(pool) < cnt:
            pool = exercises
        # Фильтрация похожих упражнений
        filtered_pool = [
            ex for ex in pool
            if not is_similar_exercise(workout, ex)
        ]
        if len(filtered_pool) < cnt:
            filtered_pool = pool
        picked = random.sample(filtered_pool, min(cnt, len(filtered_pool)))
        for ex in picked:
            ex = dict(ex)
            ex["repetitions"] = select_reps(ex, load_level)
            workout.append(ex)
        return workout

    # 4. КРОССФИТ
    if sport_id == get_sport_id("кроссфит"):
        # Кроссфит всегда состоит из блоков: разминка, Навыки/Сила, WOD, заминка
        # 1. Разминка
        group_id = get_group_id(sport_id, "разминка")
        if group_id:
            warmup = get_exercises_by_group(group_id)
            if warmup:
                ex = dict(random.choice(warmup))
                ex["repetitions"] = select_reps(ex, load_level)
                ex["block"] = "разминка"
                workout.append(ex)
        # 2. Навыки/Сила — случайно выбрать одну из подходящих групп
        skill_groups = [
            "рывковые упражнения",
            "толчковые упражнения",
            "жимовые упражнения",
            "ноги"
        ]
        sg = random.choice(skill_groups)
        group_id = get_group_id(sport_id, sg)
        if group_id:
            skills = get_exercises_by_group(group_id)
            if skills:
                ex = dict(random.choice(skills))
                ex["repetitions"] = select_reps(ex, load_level)
                ex["block"] = "навыки/сила"
                workout.append(ex)
        # 3. WOD (тренировка дня)
        group_id = get_group_id(sport_id, "WOD")
        if group_id:
            wod_exs = get_exercises_by_group(group_id)
            if wod_exs:
                ex = dict(random.choice(wod_exs))
                ex["repetitions"] = select_reps(ex, load_level)
                ex["block"] = "WOD"
                workout.append(ex)
        # 4. Заминка
        group_id = get_group_id(sport_id, "заминка")
        if group_id:
            finish = get_exercises_by_group(group_id)
            if finish:
                ex = dict(random.choice(finish))
                ex["repetitions"] = select_reps(ex, load_level)
                ex["block"] = "заминка"
                workout.append(ex)
        return workout

    # Фолбэк: случайно 4 упражнения
    rows = get_exercises_for_sport(sport_id)
    pool = [r for r in rows if r["id"] not in last_ids]
    if len(pool) < 4:
        pool = rows
    # Фильтрация похожих упражнений
    filtered_pool = [
        ex for ex in pool
        if not is_similar_exercise(workout, ex)
    ]
    if len(filtered_pool) < 4:
        filtered_pool = pool
    picked = random.sample(filtered_pool, min(4, len(filtered_pool)))
    workout = []
    for row in picked:
        ex = dict(row)
        ex["repetitions"] = select_reps(ex, load_level)
        workout.append(ex)
    return workout


def select_reps(ex, load_level):
    if load_level == "лёгкий":
        return ex["reps_light"]
    elif load_level == "средний":
        return ex["reps_medium"]
    else:
        return ex["reps_heavy"]
