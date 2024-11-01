# таблица для хранения настроек
from src.database.connection import db_session


async def create_tables():
    async with db_session() as session:
        await session.execute('''CREATE TABLE IF NOT EXISTS welcome_message (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL
        )''')
        await session.execute('''CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY,
            user_full_name TEXT NOT NULL
        )''')
        await session.execute(
            '''CREATE TABLE IF NOT EXISTS buttons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT NOT NULL,
                type TEXT CHECK(type IN ('static', 'dynamic') NOT NULL)
                )
            '''
        )
        await session.execute('''CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dynamic_button_count INTEGER
        )''')
        await session.execute(
            '''INSERT OR IGNORE INTO settings (id, dynamic_button_count) VALUES (1, 0)''')
        await session.commit()
