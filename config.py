import os

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

# Данные для подключения к базе данных PostgreSQL
DATABASE_URL = "postgresql://my_user:Matveev@localhost:5432/Fitness_bot"

# API ключи для различных платёжных систем
COINBASE_COMMERCE_API_KEY = os.getenv("COINBASE_COMMERCE_API_KEY")
BITPAY_API_KEY = os.getenv("BITPAY_API_KEY")
CRYPTOCOM_API_KEY = os.getenv("CRYPTOCOM_API_KEY")
