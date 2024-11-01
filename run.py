import asyncio

from aiogram import Dispatcher
from src.config import bot
from src.database.repository.createtables import create_tables

from src.handlers.admin import router as admin_router
from src.handlers.join2group import router as join2group_router
from src.handlers.start import router as start_router
from src.config import logger


async def main():
    await create_tables()
    dp = Dispatcher()
    dp.include_routers(admin_router, join2group_router, start_router)

    r = await bot.get_me()
    logger.info(f"Бот запущен: https://t.me/{r.username}")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
