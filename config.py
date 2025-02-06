# config.py
import os
from dotenv import load_dotenv
from logger import get_logger

# Загружаем переменные окружения из .env
load_dotenv()

# Инициализация логгера
logger = get_logger()

# Читаем токены из переменных окружения
API_TOKEN = os.getenv("API_TOKEN")
COINBASE_COMMERCE_API_KEY = os.getenv("COINBASE_COMMERCE_API_KEY")
BITPAY_API_KEY = os.getenv("BITPAY_API_KEY")
CRYPTOCOM_API_KEY = os.getenv("CRYPTOCOM_API_KEY")

# Данные для подключения к базе данных PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://my_user:Matveev@localhost:5432/Fitness_bot")

# Проверка API-токенов
def check_required_tokens():
    missing_tokens = []

    if not API_TOKEN:
        missing_tokens.append("API_TOKEN")
    # if not COINBASE_COMMERCE_API_KEY:
    #     missing_tokens.append("COINBASE_COMMERCE_API_KEY")
    # if not BITPAY_API_KEY:
    #     missing_tokens.append("BITPAY_API_KEY")
    # if not CRYPTOCOM_API_KEY:
    #     missing_tokens.append("CRYPTOCOM_API_KEY")

    if missing_tokens:
        logger.critical(f"Отсутствуют необходимые токены: {', '.join(missing_tokens)}")
        raise ValueError(f"Не заданы переменные окружения: {', '.join(missing_tokens)}")

# Запускаем проверку токенов
try:
    check_required_tokens()
    logger.info("Все API-токены загружены успешно.")
except ValueError as e:
    logger.critical(str(e))
    exit(1)  # Остановить выполнение программы, если критически важные токены отсутствуют
