from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.config import BOT_ADMIN_ID
from src.states.admin import FSM_DynamicButtons, FSM_admin_panel
from src.utils.keyboards.admin import admin_panel_kb
from src.utils.welcome_message import configure_welcome_message
from src.database.models import DbSettings
from src.states.admin import FSM_admin_panel

router = Router()


@router.message(F.text == 'Посмотреть приветственное сообщение')
async def get_welcome_message_handler(message: Message):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только для администратора')
        await message.delete()
        return

    welcome_message = await configure_welcome_message(
        user_full_name=message.from_user.full_name,
        username=message.from_user.username,
        user_id=message.from_user.id,
    )

    if welcome_message:
        await message.answer(
            text=welcome_message,
            reply_markup=admin_panel_kb
        )
    else:
        await message.answer('Приветственное сообщение не найдено.')


@router.message(F.text == 'Отредактировать приветственное сообщение')
async def edit_welcome_message(message: Message, state: FSMContext):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только для администратора')
        await message.delete()
        return
    await message.answer('Пожалуйста, отправьте новое приветственное сообщение:')
    await state.set_state(FSM_admin_panel.get_message)


@router.message(FSM_admin_panel.get_message)
async def handle_new_welcome_message(message: Message, state: FSMContext):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только для администратора')
        await message.delete()
        return

    await DbSettings.set_settings(welcome_message=message.text)
    await message.answer('Приветственное сообщение обновлено.')
    await state.clear()


@router.message(F.text == 'Установить количество динамических кнопок')
async def dynamic_buttons(message: Message, state: FSMContext):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только для администратора')
        await message.delete()
        return


@router.message(FSM_admin_panel.get_amount_of_dynamic_buttons)
async def get_amount_of_dynamic_buttons(message: Message, state: FSMContext):
    ...


# Работа с динамическими кнопками
@router.message(F.text == 'динамические кнопки')
async def dynamic_buttons_menu(message: Message, state: FSMContext):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только для администратора')
        await message.delete()
        return


@router.message(F.text == 'Добавить новую кнопку',
                FSM_DynamicButtons.working_with_buttons)
async def prompt_button_name(message: Message, state: FSMContext):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только для администратора')
        await message.delete()
        return


@router.message(FSM_DynamicButtons.get_button_name)
async def receive_button_name(message: Message, state: FSMContext):
    button_name = message.text
    if len(button_name) > 20:
        await message.answer(
            'Сделай название кнопки поменьше (не более 20 символов), '
            'а то слишком длинное'
        )
        return
    ...


@router.message(FSM_DynamicButtons.get_button_link)
async def receive_button_link(message: Message, state: FSMContext):
    ...


@router.message(F.text == 'Получить список всех кнопок',
                FSM_DynamicButtons.working_with_buttons)
async def get_all_buttons(message: Message):  # static or dynamic?
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только для администратора')
        await message.delete()
        return


@router.message(FSM_DynamicButtons.working_with_buttons,
                F.text == 'Удалить лишние кнопки')
async def delete_buttons(message: Message):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только для администратора')
        await message.delete()
        return


@router.callback_query(lambda c: c.data.startswith('del:'))
async def process_delete_button(callback_query: CallbackQuery):
    ...


@router.message(F.text == 'статические кнопки')
async def static_button(message: Message, state: FSMContext):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только для администратора')
        await message.delete()
        return
