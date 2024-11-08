from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.config import logger
from src.config import BOT_ADMIN_ID
from src.database.models import DbUser
from src.utils.keyboards.admin import admin_panel_kb

router = Router()


@router.message(Command('start'), F.chat.type == 'private')
async def start(message: Message, state: FSMContext):
    if not await DbUser.get_user(user_id=message.from_user.id):
        await DbUser.add_user(
            user_id=message.from_user.id,
            full_name=message.from_user.first_name
        )
        logger.debug(
            f'Пользователь({message.from_user.full_name}) c id: {message.from_user.id} добавлен в базу данных')

        await message.answer(
            'Привет, ты новенький, видимо, этот бот доступен только админам '
            'Когда-нибудь потом мы будем через него делать рассылки'
        )
    else:
        if message.chat.type == 'private' and message.from_user.id == BOT_ADMIN_ID:
            await message.answer(
                text = 'Привет! '
                       'Тут ты можешь настроить приветственное сообщение',
                reply_markup = admin_panel_kb
            )
    await message.delete()
