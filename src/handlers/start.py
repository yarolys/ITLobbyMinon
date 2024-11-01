from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.config import logger
from src.config import BOT_ADMIN_ID
from src.database.models import User
router = Router()


# является человек админом или нет если нет только для админа

@router.message(Command('start'))
@router.message(F.text == 'Вернуться в меню')
async def start(message: Message, state: FSMContext):
    if not await User.get_user(user_id=message.from_user.id):
        await User.add_user(
            user_id=message.from_user.id,
            full_name=message.from_user.first_name
        )
        logger.debug(f'Пользователь({message.from_user.full_name}) c id: {message.from_user.id} добавлен в базу данных')

        await message.answer(
            'Привет, ты новенький, видимо, этот бот доступен только админам'
            'Когда-нибудь потом мы будем через него делать рассылки'
        )
    elif message.from_user.id != BOT_ADMIN_ID:
        await message.answer(
            'Повторюсь, тебе сюда низя'
        )
    if message.from_user.id == BOT_ADMIN_ID and message.chat.type == 'private':
        ...
        # тута отправляем клавиатуру админской панели
    #
    # if message.chat.type == 'private' and message.from_user.id == BOT_ADMIN_ID:
    #     await message.answer(
    #         text='Салам пополам!\nТут ты короче можешь настроить приветственное сообщение',
    #         reply_markup=admin_panel_kb
    #     )
    # else:
    #     await message.answer(
    #         text='Ты конечно красавчик, что хочешь воспользоваться ботом, но доступ к нему есть только'
    #              'у владельца - @KandyBobby'
    #     )
    # await state.clear()
