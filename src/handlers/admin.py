from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.states.admin import FSM_DynamicButtons, FSM_admin_panel

router = Router()


@router.message(F.text == 'Посмотреть приветственное сообщение')
async def get_welcome_message(message: Message):
    ...


@router.message(F.text == 'Отредактировать приветственное сообщение')
async def edit_welcome_message(message: Message, state: FSMContext):
    ...


@router.message(FSM_admin_panel.get_message)
async def handle_new_welcome_message(message: Message, state: FSMContext):
    ...


@router.message(F.text == 'Установить количество динамических кнопок')
async def dynamic_buttons(message: Message, state: FSMContext):
    ...


@router.message(FSM_admin_panel.get_amount_of_dynamic_buttons)
async def get_amount_of_dynamic_buttons(message: Message, state: FSMContext):
    ...


# Работа с динамическими кнопками
@router.message(F.text == 'динамические кнопки')
async def dynamic_buttons_menu(message: Message, state: FSMContext):
    ...


@router.message(F.text == 'Добавить новую кнопку',
                FSM_DynamicButtons.working_with_buttons)
async def prompt_button_name(message: Message, state: FSMContext):
    ...


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
    ...


@router.message(FSM_DynamicButtons.working_with_buttons,
                F.text == 'Удалить лишние кнопки')
async def delete_buttons(message: Message):
    ...


@router.callback_query(lambda c: c.data.startswith('del:'))
async def process_delete_button(callback_query: CallbackQuery):
    ...


@router.message(F.text == 'статические кнопки')
async def static_button(message: Message, state: FSMContext):
    ...
