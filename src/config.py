# тут создаём экземпляр бота, переменные итд
import os

from aiogram import Bot
from dotenv import load_dotenv
from loguru import logger


load_dotenv()

logger.add(
        'logs/log.log',
        format='{time:yyyy-MM-dd HHH:mm:ss} {level} {message}',
        level='DEBUG',
        rotation='50 MB'
)

TOKEN = os.getenv('TOKEN')
bot = Bot(
        token=TOKEN
)
BOT_ADMIN_ID = int(os.getenv('BOT_ADMIN_ID'))

DATABASE_URL = 'database.db'
