import os

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
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
        token=TOKEN,
        default=DefaultBotProperties(parse_mode='HTML')
)
BOT_ADMIN_ID = int(os.getenv('BOT_ADMIN_ID'))

