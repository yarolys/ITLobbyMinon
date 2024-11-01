# подключение к БД
import aiosqlite
from src.config import DATABASE_URL
from contextlib import asynccontextmanager


@asynccontextmanager
async def db_session():
    connection = await aiosqlite.connect(DATABASE_URL)
    try:
        yield connection
    finally:
        await connection.close()


async def set_amount_of_dynamic_buttons(amount: int):
    query = "UPDATE settings SET dynamic_button_count = ? WHERE id = 1"
    async with db_session() as session:
        await session.execute(query, (amount,))
        await session.commit()


async def get_all_buttons():
    async with db_session() as session:
        cursor = await session.execute("SELECT name, url FROM buttons")
        buttons = await cursor.fetchall()
        return buttons
