from src.database.repository.createtables import db_session


async def add_button(name, url):
    async with db_session() as session:
        await session.execute('INSERT INTO buttons (name, url) VALUES (?, ?)',
                              (name, url))
        await session.commit()


async def get_buttons():
    async with db_session() as session:
        async with session.execute('SELECT * FROM buttons') as cursor:
            return await cursor.fetchall()


async def remove_button(name):
    async with db_session() as session:
        await session.execute('DELETE FROM buttons WHERE name = ?', (name,))
        await session.commit()
        return 0


async def get_static_buttons():
    async with db_session() as session:
        async with session.execute(
                'SELECT * FROM buttons WHERE type = "static"') as cursor:
            return await cursor.fetchall()
