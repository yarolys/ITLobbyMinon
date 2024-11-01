from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.chemas import KbButton
from src.database.repository import button


async def welcome_message_kb_without_urls():
    buttons_dct = await button.get_buttons()
    keyboard_2 = InlineKeyboardBuilder()
    for button_id, button_data in buttons_dct:
        keyboard_2.button(text=button_data["name"], callback_data=button_id)
    keyboard_2.adjust(1)
    return keyboard_2.as_markup()


async def generate_keyboard_with_urls(buttons: list[KbButton]):
    """
    Creates an inline keyboard with URL buttons.

    :param buttons: List of KbButton objects, each with 'name' (button text) and 'url' (link).
    :return: Inline keyboard markup with the specified buttons.
    """
    keyboard = InlineKeyboardBuilder()
    for kb_button in buttons:
        keyboard.button(text=kb_button.name, url=kb_button.url)
    keyboard.adjust(1)
    return keyboard.as_markup()
