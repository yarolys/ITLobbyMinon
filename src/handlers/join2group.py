from aiogram import F, Router
from aiogram.types import Message
from src.config import logger
from src.database.repository.welcomemessage import get_welcome_message_text
router = Router()


@router.message(F.new_chat_members)
async def welcome_new_member(message: Message):
    for new_member in message.new_chat_members:
        logger.info(f"Новый участник: {new_member.full_name}")
        welcome_message = await get_welcome_message_text()

        await message.answer(
            text=welcome_message,
        )
