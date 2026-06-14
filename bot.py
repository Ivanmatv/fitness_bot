import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import API_TOKEN
from handlers.start_handler import router as start_router
from handlers.gender_handler import router as gender_router
from handlers.sport_handler import router as sport_router
from handlers.intensity_handler import router as intensity_router

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_router(start_router)
dp.include_router(gender_router)
dp.include_router(sport_router)
dp.include_router(intensity_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())