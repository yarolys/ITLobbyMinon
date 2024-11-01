import aiosqlite

from src.database.connection import db_session
from src.config import logger


async def get_welcome_message_text():
    async with aiosqlite.connect("database.db") as db:
        async with db.execute(
                "SELECT message FROM welcome_message WHERE id = 1") as cursor:
            row = await cursor.fetchone()
        return row[0] if row else None


async def update_welcome_message(new_message: str):
    async with db_session() as session:
        result = await session.execute("SELECT * FROM welcome_message WHERE id = 1")
        existing_message = await result.fetchone()

        if existing_message is None:
            logger.debug('Сообщение отсутствует')
            await session.execute(
                "INSERT INTO welcome_message (id, message) VALUES (1, ?)",
                (new_message,))
        else:
            logger.debug('обновили сообщение')
            await session.execute("UPDATE welcome_message SET message = ? WHERE id = 1",
                                  (new_message,))
        await session.commit()
        return new_message
