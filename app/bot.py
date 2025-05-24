import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from handlers import register_handlers
from database import init_db
from logger import get_logger

logger = get_logger()


async def main():
    init_db()
    logger.info("База данных инициализирована")
    storage = MemoryStorage()
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=storage)
    register_handlers(dp)
    logger.info("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
