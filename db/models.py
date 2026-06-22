from sqlalchemy import (
    Column, Integer, String,
    Boolean, ForeignKey,
    Text, DateTime
)
from sqlalchemy.orm import relationship
from datetime import datetime

from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    gender = Column(String(1), nullable=False)
    subscription_status = Column(Boolean, default=False)
    workouts = relationship("Workout", back_populates="user")


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    sport_id = Column(Integer, ForeignKey('sports.id'), nullable=False)
    intensity_id = Column(Integer, ForeignKey('intensity_levels.id'), nullable=False)
    rest_recommendation = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="workouts")
    sport = relationship("Sport", back_populates="workouts")
    intensity = relationship("IntensityLevel", back_populates="workouts")
    workout_exercises = relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey('workouts.id'), nullable=False)
    exercise_id = Column(Integer, ForeignKey('exercises.id'), nullable=False)
    exercise_order = Column(Integer, nullable=False)   # порядковый номер упражнения в тренировке
    exercise_count = Column(Integer, nullable=False)
    workout = relationship("Workout", back_populates="workout_exercises")
    exercise = relationship("Exercise")


class ExerciseType(Base):
    __tablename__ = "exercise_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    exercises = relationship("Exercise", back_populates="exercise_type")


class Sport(Base):
    __tablename__ = "sports"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    exercises = relationship("Exercise", back_populates="sport")
    workouts = relationship("Workout", back_populates="sport")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    sport_id = Column(Integer, ForeignKey('sports.id'), nullable=False)
    exercise_type_id = Column(Integer, ForeignKey('exercise_types.id'), nullable=False)
    sport = relationship("Sport", back_populates="exercises")
    exercise_type = relationship("ExerciseType", back_populates="exercises")


class IntensityLevel(Base):
    __tablename__ = "intensity_levels"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    workouts = relationship("Workout", back_populates="intensity")