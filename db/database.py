# database.py
from psycopg2 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from logger import get_logger

logger = get_logger()

# Путь к базе данных для PostgreSQL
DATABASE_URL = "postgresql://postgres:root@localhost:5432/Fitness_bot"

# Создание движка базы данных
engine = create_engine(DATABASE_URL)

# Создание базового класса для моделей
Base = declarative_base()

connection = engine.connect()

# Создание сессии для взаимодействия с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Функция для создания всех таблиц
def create_tables():
    try:
        # Создание всех таблиц
        Base.metadata.create_all(bind=engine)
        logger.info("Successfully connected to the database and created tables.")
    except OperationalError as e:
        logger.error(f"OperationalError: {e}")
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")