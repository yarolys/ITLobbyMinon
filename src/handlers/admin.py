from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from src.config import BOT_ADMIN_ID
from src.database.models.butons import Button
from src.schemas import ButtonTypeEnum
from src.states.admin import FSM_DynamicButtons, FSM_admin_panel
from src.utils.keyboards.admin import admin_panel_kb, edit_buttons_kb, working_with_buttons_kb
from src.utils.welcome_message import configure_welcome_message
from src.database.models import DbSettings

import aiohttp


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


# Работа с динамическими кнопками
@router.message(F.text == 'динамические кнопки')
async def dynamic_buttons_menu(message: Message):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только для администратора')
        await message.delete()
        return
    await message.answer(text='Здесь ты можешь редактировать динамические кнопки',
    reply_markup=edit_buttons_kb,
    )


@router.message(F.text == 'Вернуться в меню')
async def back_to_main(message: Message):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только для администратора')
        await message.delete()
        return
    await message.answer(
        text='Ты вернулся в главное меню',
        reply_markup=admin_panel_kb
    )


@router.message(F.text == 'Установить количество динамических кнопок')
async def dynamic_buttons(message: Message):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только для администратора')
        await message.delete()
        return
    ...


@router.message(FSM_admin_panel.get_amount_of_dynamic_buttons)
async def get_amount_of_dynamic_buttons():
    ...


async def check_url_accessibility(url: str) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url, timeout=5) as response:
                if response.status < 400:
                    return True
                else:
                    return False
    except Exception as e:
        logger.error(f"Ошибка при проверке доступности URL: {e}")
        return False

@router.message(F.text == 'Добавить динамическую кнопку')
async def prompt_button_name(message: Message, state: FSMContext):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только для администратора')
        await message.delete()
        return

    await state.set_state(FSM_DynamicButtons.get_button_name)
    await message.answer('Введите название кнопки (не более 20 символов):')

@router.message(FSM_DynamicButtons.get_button_name)
async def process_button_name(message: Message, state: FSMContext):
    button_name = message.text

    if len(button_name) > 20:
        await message.answer('Название кнопки должно быть не более 20 символов.')
        return

    await state.update_data(button_name=button_name)
    await state.set_state(FSM_DynamicButtons.get_button_link)
    await message.answer("Теперь введите URL кнопки начиная с http:// или https://")

@router.message(FSM_DynamicButtons.get_button_link)
async def process_button_url(message: Message, state: FSMContext):
    button_url = message.text

    if len(button_url) > 40 or not button_url.startswith(('http://', 'https://')):
        await message.answer('Ссылка должна быть не более 40 символов и начинаться с http:// или https://.')
        return

    is_accessible = await check_url_accessibility(button_url)
    if not is_accessible:
        await message.answer('Ссылка недоступна или ведет на несуществующий ресурс.')
        return

    data = await state.get_data()
    button_name = data.get("button_name")


    await Button.add_button(name=button_name, url=button_url, type=ButtonTypeEnum.dynamic)
    await message.answer(f"Кнопка '{button_name}' успешно добавлена.")

    await state.clear()



@router.message(F.text == 'Получить список всех кнопок')
async def show_all_buttons(message: Message):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только для администратора')
        await message.delete()
        return
    buttons = await Button.get_all_buttons()
    if not buttons:
        await message.answer("Список кнопок пуст.")
        return
    keyboard_buttons = [
        [InlineKeyboardButton(text=button.name, url=str(button.url))]
        for button in buttons
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await message.answer("Список всех кнопок:", reply_markup=keyboard)


@router.message(F.text == 'Удалить лишние кнопки')
async def delete_extra_buttons(message: Message):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только для администратора')
        await message.delete()
        return

    buttons = await Button.get_all_buttons()
    if not buttons:
        await message.answer("Нет кнопок для удаления.")
        return

    keyboard_buttons = [
        [InlineKeyboardButton(text=button.name, callback_data=f'del:{button.id}')]
        for button in buttons
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    await message.answer("Выберите кнопку для удаления:", reply_markup=keyboard)



@router.callback_query(lambda c: c.data.startswith('del:'))
async def process_delete_button(callback_query: CallbackQuery):
    button_id = int(callback_query.data[len('del:'):])
    success = await Button.delete_button(button_id)

    if success:
        await callback_query.answer(f"Кнопка с ID {button_id} успешно удалена.")
    else:
        await callback_query.answer("Не удалось найти кнопку для удаления.")
    await callback_query.message.delete()


@router.message(F.text == 'статические кнопки')
async def static_button(message: Message):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только для администратора')
        await message.delete()
        return
    await message.answer(
        text='Ты находишься в редакторе статических кнопок',
        reply_markup=working_with_buttons_kb
    )


@router.message(F.text == 'Добавить статическую кнопку')
async def add_static_button(message: Message, state: FSMContext):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer("Только для администратора.")
        await message.delete()
        return

    await state.update_data(button_type=ButtonTypeEnum.static)
    await state.set_state(FSM_DynamicButtons.get_button_name)
    await message.answer("Введите название статической кнопки (не более 20 символов):")


@router.message(FSM_DynamicButtons.get_button_name)
async def process_button_name(message: Message, state: FSMContext):
    button_name = message.text
    if len(button_name) > 20:
        await message.answer("Название кнопки должно быть не более 20 символов.")
        return

    await state.update_data(button_name=button_name)
    await state.set_state(FSM_DynamicButtons.get_button_link)
    await message.answer("Теперь введите URL кнопки, начиная с http:// или https://")


@router.message(FSM_DynamicButtons.get_button_link)
async def process_button_url(message: Message, state: FSMContext):
    button_url = message.text
    if len(button_url) > 40 or not button_url.startswith(("http://", "https://")):
        await message.answer("Ссылка должна быть не более 40 символов и начинаться с http:// или https://.")
        return
    is_accessible = await check_url_accessibility(button_url)
    if not is_accessible:
        await message.answer("Ссылка недоступна или ведет на несуществующий ресурс.")
        return

    data = await state.get_data()
    button_name = data.get("button_name")
    button_type = data.get("button_type")

    await Button.add_button(name=button_name, url=button_url, type=button_type)
    await message.answer(
        f"Кнопка '{button_name}' успешно добавлена как {'статическая' if button_type == ButtonTypeEnum.static else 'динамическая'}.")

    await state.clear()


@router.message(F.text == 'Получить список всех кнопок')
async def show_all_buttons(message: Message):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer("Только для администратора.")
        await message.delete()
        return

    buttons = await Button.get_all_buttons()
    if not buttons:
        await message.answer("Список кнопок пуст.")
        return


    static_btns = [button for button in buttons if button.type == ButtonTypeEnum.static]
    dynamic_btns = [button for button in buttons if button.type == ButtonTypeEnum.dynamic]
    sorted_buttons = static_btns + dynamic_btns


    keyboard_buttons = [
        [InlineKeyboardButton(text=button.name, url=str(button.url))] for button in sorted_buttons
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await message.answer("Список всех кнопок:", reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith('del:'))
async def process_delete_button(callback_query: CallbackQuery):
    try:
        button_id = int(callback_query.data.split(':')[1])
        success = await Button.delete_button(button_id)

        if success:
            await callback_query.answer(f"Кнопка с ID {button_id} успешно удалена.")
        else:
            await callback_query.answer("Не удалось найти кнопку для удаления.")
    except ValueError:
        await callback_query.answer("Некорректный формат ID кнопки.")

    await callback_query.message.delete()