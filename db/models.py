# models.py
from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base


class User(Base):
    """Пользователь"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    gender = Column(Enum('M', 'F', name='gender_enum'), nullable=False)
    sport = Column(Enum('fitness', 'powerlifting', 'weightlifting', 'crossfit', name='sport_enum'), nullable=False)
    intensity = Column(Enum('light', 'medium', 'heavy', name='intensity_enum'), nullable=False)
    subscription_status = Column(Boolean, default=False)
    workouts = relationship("Workout", back_populates="user")


class Workout(Base):
    """Тренировки пользователя."""
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True)
    exercises = Column(Text, nullable=False)  # Можно хранить список упражнений в JSON
    rest_recommendation = Column(String, nullable=True)  # Рекомендации по отдыху
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="workouts")


class ExerciseType(Base):
    """Тип тренировок(кардио, силовые, растяжка)."""
    __tablename__ = "exercise_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    exercises = relationship("Exercise", back_populates="exercise_type")


class Sport(Base):
    """Вид спорта(ТА, ПА, фитнес)"""
    __tablename__ = "sports"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    exercises = relationship("Exercise", back_populates="sport")


class Exercise(Base):
    """Упражнения."""
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)  # Ссылка на изображение упражнения
    sport_id = Column(Integer, ForeignKey('sports.id'), nullable=False)
    exercise_type_id = Column(Integer, ForeignKey('exercise_types.id'), nullable=False)
    sport = relationship("Sport", back_populates="exercises")
    exercise_type = relationship("ExerciseType", back_populates="exercises")
