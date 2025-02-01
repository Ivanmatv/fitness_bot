from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

# Модель пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    gender = Column(Enum('M', 'F', name='gender_enum'), nullable=False)  # Пол
    sport = Column(Enum('fitness', 'powerlifting', 'weightlifting', 'crossfit', name='sport_enum'), nullable=False)  # Вид спорта
    intensity = Column(Enum('light', 'medium', 'heavy', name='intensity_enum'), nullable=False)  # Уровень нагрузки
    subscription_status = Column(Boolean, default=False)  # Статус подписки (платная или нет)

    workouts = relationship("Workout", back_populates="user")  # Связь с тренировками

# Модель тренировки
class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True)
    exercises = Column(String, nullable=False)  # Упражнения в тренировке (например, через строку)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Ссылка на пользователя

    user = relationship("User", back_populates="workouts")  # Связь с пользователем

# Типы упражнений (например, силовые, кардио)
class ExerciseType(Base):
    __tablename__ = "exercise_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # Название типа (например, "силовые", "кардио")

    exercises = relationship("Exercise", back_populates="exercise_type")  # Связь с упражнениями

# Виды спорта (например, фитнес, пауэрлифтинг)
class Sport(Base):
    __tablename__ = "sports"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # Название вида спорта (например, "фитнес", "пауэрлифтинг")

    exercises = relationship("Exercise", back_populates="sport")  # Связь с упражнениями

# Упражнения, привязанные к конкретному виду спорта и типу
class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # Название упражнения (например, "жим лёжа", "подтягивания")
    description = Column(String, nullable=True)  # Описание упражнения (по желанию)
    sport_id = Column(Integer, ForeignKey('sports.id'), nullable=False)  # Ссылка на вид спорта
    exercise_type_id = Column(Integer, ForeignKey('exercise_types.id'), nullable=False)  # Ссылка на тип упражнения

    sport = relationship("Sport", back_populates="exercises")  # Связь с видом спорта
    exercise_type = relationship("ExerciseType", back_populates="exercises")  # Связь с типом упражнения
