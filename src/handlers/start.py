from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command


from src.config import logger
from src.database.models import DbUser
from src.config import BOT_ADMIN_ID


router = Router()

@router.message(Command('start'), F.chat.type == 'private')
async def start(message: Message):
    if not await DbUser.get_user(user_id=message.from_user.id):
        await DbUser.add_user(
            user_id=message.from_user.id,
            full_name=message.from_user.first_name
        )
        logger.debug(
            f'Пользователь({message.from_user.full_name}) с id: {message.from_user.id} добавлен в БД')

    if message.from_user.id == BOT_ADMIN_ID:
        await message.answer('Для запуска админки нажми /admin')
    else:
        await message.answer(
            'Салам, пока что этот бот доступен только для администраторов, позже мы будем '
            'делать рассылки через него'
        )

    await message.delete()