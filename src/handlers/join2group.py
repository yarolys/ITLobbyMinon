from aiogram import F, Router
from aiogram.types import Message

from src.database import repository
from src.keyboards.join2group import welcome_message_kb

router = Router()


@router.message(F.new_chat_members)
async def welcome_new_member(message: Message):
    welcome_message = repository.get_welcome_message_text(message)  # TODO: Fix
    await message.answer(
        text=welcome_message,
        reply_markup=welcome_message_kb(),
    )
