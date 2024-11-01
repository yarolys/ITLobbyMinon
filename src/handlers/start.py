from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.config import BOT_ADMIN_ID
from src.keyboards.admin import admin_panel_kb

router = Router()


# является человек админом или нет если нет только для админа

@router.message(Command('start'))
@router.message(F.text == 'Вернуться в меню')
async def start(message: Message, state: FSMContext):
    if message.chat.type == 'private' and message.from_user.id == BOT_ADMIN_ID:
        await message.answer(
            text='Салам пополам!\nТут ты короче можешь настроить приветственное сообщение',
            reply_markup=admin_panel_kb
        )
    else:
        await message.answer(
            text='Ты конечно красавчик, что хочешь воспользоваться ботом, но доступ к нему есть только'
                 'у владельца - @KandyBobby'
        )
    await state.clear()
