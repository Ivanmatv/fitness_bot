import sqlite3

from config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        gender TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        sport_id INTEGER,
        load_level TEXT,
        description TEXT,
        reps_light TEXT,
        reps_medium TEXT,
        reps_heavy TEXT,
        FOREIGN KEY (sport_id) REFERENCES sports(id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        sport_id INTEGER,
        load_level TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (sport_id) REFERENCES sports(id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workout_exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        workout_id INTEGER,
        exercise_id INTEGER,
        FOREIGN KEY (workout_id) REFERENCES workouts(id),
        FOREIGN KEY (exercise_id) REFERENCES exercises(id)
    )""")

    # Добавляем виды спорта, если их нет
    sports = ['фитнес', 'пауэрлифтинг', 'тяжёлая атлетика', 'кроссфит']
    for sport in sports:
        cursor.execute("INSERT OR IGNORE INTO sports (name) VALUES (?)", (sport,))

    conn.commit()
    conn.close()


def add_user(telegram_id, gender):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (telegram_id, gender) VALUES (?, ?)", (telegram_id, gender))
    conn.commit()
    conn.close()


def get_user(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def add_workout(user_id, sport_id, load_level, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO workouts (user_id, sport_id, load_level, date) VALUES (?, ?, ?, ?)",
        (user_id, sport_id, load_level, date)
    )
    workout_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return workout_id


def add_workout_exercise(workout_id, exercise_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO workout_exercises (workout_id, exercise_id) VALUES (?, ?)", (workout_id, exercise_id))
    conn.commit()
    conn.close()


def get_sport_id(sport_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM sports WHERE name = ?", (sport_name,))
    sport = cursor.fetchone()
    conn.close()
    return sport['id'] if sport else None


def get_exercises_for_sport_and_load(sport_id, load_level):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM exercises WHERE sport_id = ? AND load_level = ?",
        (sport_id, load_level)
    )
    exercises = cursor.fetchall()
    conn.close()
    return exercises


def get_last_workout_exercises(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id FROM exercises e
        JOIN workout_exercises we ON e.id = we.exercise_id
        JOIN workouts w ON we.workout_id = w.id
        WHERE w.user_id = ?
        ORDER BY w.date DESC LIMIT 1
    """, (user_id,))
    exercises = cursor.fetchall()
    conn.close()
    return [e['id'] for e in exercises] if exercises else []


def get_workout_history(user_id):
    """Возвращает список всех тренировок пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    # Получаем все тренировки пользователя
    cursor.execute("""
        SELECT w.id, w.date, s.name AS sport, w.load_level
        FROM workouts w
        JOIN sports s ON w.sport_id = s.id
        WHERE w.user_id = ?
        ORDER BY w.date DESC
    """, (user_id,))
    workouts = cursor.fetchall()

    history = []
    for w in workouts:
        # Для каждой тренировки берём упражнения
        cursor.execute("""
            SELECT e.name, e.description,
                   e.reps_light, e.reps_medium, e.reps_heavy
            FROM workout_exercises we
            JOIN exercises e ON we.exercise_id = e.id
            WHERE we.workout_id = ?
        """, (w['id'],))
        exercises = cursor.fetchall()

        ex_list = []
        for ex in exercises:
            if w['load_level'] == 'лёгкий':
                reps = ex['reps_light']
            elif w['load_level'] == 'средний':
                reps = ex['reps_medium']
            else:
                reps = ex['reps_heavy']
            ex_list.append({
              'name': ex['name'],
              'description': ex['description'],
              'repetitions': reps
            })

        history.append({
            'date': w['date'],
            'sport': w['sport'],
            'load': w['load_level'],
            'exercises': ex_list
        })

    conn.close()
    return history
