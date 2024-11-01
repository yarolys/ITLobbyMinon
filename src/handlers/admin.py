from aiogram import F, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from aiogram.fsm.context import FSMContext
from src.config import BOT_ADMIN_ID, logger
from src.database.connection import db_session
from src.database.repository.button import add_button, remove_button
from src.database.repository.welcomemessage import get_welcome_message_text, \
    update_welcome_message
from src.keyboards.admin import working_with_buttons_kb
from src.states.admin import FSM_admin_panel, FSM_DynamicButtons
import asyncio

router = Router()


@router.message(F.text == 'Посмотреть приветственное сообщение')
async def get_welcome_message(message: Message):
    """
    Get welcome message to admin
    :param message: Message
    :return: None
    """
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только для администратора')
        await message.delete()
        return

    welcome_message = await get_welcome_message_text()
    if welcome_message:
        await message.answer(text=welcome_message)
    else:
        await message.answer(text='Приветственное сообщение не установлено')


@router.message(F.text == 'Отредактировать приветственное сообщение')
async def edit_welcome_message(message: Message, state: FSMContext):
    """
    Update welcome message to admin
    :param message: Message
    :return: None
    """
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только для администратора')
        await message.delete()
        return

    await message.answer(
        'Отправь текст для сообщения, которое будет использоваться как приветственное')
    await state.set_state(FSM_admin_panel.get_message)
    await message.delete()


@router.message(FSM_admin_panel.get_message)
async def handle_new_welcome_message(message: Message, state: FSMContext):
    new_welcome_message = message.text
    logger.debug(f"Получено новое приветственное сообщение: {new_welcome_message}")
    await update_welcome_message(new_welcome_message)
    await message.answer("Новое приветственное сообщение сохранено.")
    await state.clear()


@router.message(F.text == 'Установить количество динамических кнопок')
async def dynamic_buttons(message: Message, state: FSMContext):
    await message.answer('Пришли мне количество динамических кнопок (числом)')
    await state.set_state(FSM_admin_panel.get_amount_of_dynamic_buttons)


@router.message(FSM_admin_panel.get_amount_of_dynamic_buttons)
async def get_amount_of_dynamic_buttons(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
        async with db_session() as session:
            await session.execute(
                'UPDATE settings SET dynamic_button_count = ? WHERE id = 1', (amount,))
            await session.commit()
        await message.answer(f'Установлено {amount} динамических кнопок для сообщения')
    except ValueError:
        await message.answer(
            'Неверный формат. Пришлите мне количество динамических кнопок (числом).')
    finally:
        await state.clear()


# Работа с динамическими кнопками
@router.message(F.text == 'динамические кнопки')
async def dynamic_buttons_menu(message: Message, state: FSMContext):
    await state.set_state(FSM_DynamicButtons.working_with_buttons)
    await message.answer(text='Редактирование динамических кнопок',
                         reply_markup=working_with_buttons_kb)


@router.message(F.text == 'Добавить новую кнопку',
                FSM_DynamicButtons.working_with_buttons)
async def prompt_button_name(message: Message, state: FSMContext):
    await message.answer(
        "Отправьте название для кнопки (можете использовать смайлики).")
    await state.set_state(FSM_DynamicButtons.get_button_name)


@router.message(FSM_DynamicButtons.get_button_name)
async def receive_button_name(message: Message, state: FSMContext):
    button_name = message.text
    if len(button_name) > 20:
        await message.answer(
            'Сделай название кнопки поменьше (не более 20 символов), '
            'а то слишком длинное'
        )
        return
    await state.update_data(button_name=button_name)
    await message.answer("Теперь отправьте URL для кнопки.")
    await state.set_state(FSM_DynamicButtons.get_button_link)


@router.message(FSM_DynamicButtons.get_button_link)
async def receive_button_link(message: Message, state: FSMContext):
    button_url = message.text.strip()
    if not button_url.startswith("http://") and not button_url.startswith("https://"):
        await message.answer("Пожалуйста, отправьте корректный URL "
                             "(должен начинаться с http:// или https://).")
        return

    user_data = await state.get_data()
    button_name = user_data.get("button_name")
    if len(button_name) + len(button_url) > 40:
        await message.answer(
            "Сделайте название кнопки меньше, ваша ссылка слишком длинная.")
        return
    await add_button(name=button_name, url=button_url)
    await message.answer(
        f"Кнопка '{button_name}' с URL '{button_url}' добавлена в базу данных.")
    await state.clear()


@router.message(F.text == 'Получить список всех кнопок',
                FSM_DynamicButtons.working_with_buttons)
async def get_all_buttons(message: Message):  # static or dynamic?
    async with db_session() as session:
        result = await session.execute('SELECT name, url FROM buttons')
        buttons = await result.fetchall()

    if not buttons:
        await message.answer('Нет динамических кнопок в базе данных.')
        return

    button_list = '\n'.join(  # FIXME
        [f"Название: {name}, URL: {url}" for name, url in buttons]
    )

    await message.answer(f'Список динамических кнопок:\n{button_list}')


@router.message(FSM_DynamicButtons.working_with_buttons,
                F.text == 'Удалить лишние кнопки')
async def delete_buttons(message: Message):
    async with db_session() as session:
        result = await session.execute(
            'SELECT name FROM buttons')  # TODO: move to DB/repository
        buttons = await result.fetchall()

    if buttons:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])

        for button in buttons:
            button_name = button[0]
            callback_data = f"del:{button_name}"

            keyboard.inline_keyboard.append(
                [InlineKeyboardButton(text=button_name, callback_data=callback_data)]
            )

        r = await message.answer(
            text='!!!Режим удаления кнопок!!!\n\n'
                 'Нажми на кнопку, чтобы удалить её:',
            reply_markup=keyboard
        )

        await asyncio.sleep(30)
        await r.delete()
    else:
        await message.answer(text='Нет доступных кнопок для удаления.')


@router.callback_query(lambda c: c.data.startswith('del:'))
async def process_delete_button(callback_query: CallbackQuery):
    button_name = callback_query.data.split(':')[1]
    rows_deleted = await remove_button(button_name)
    if rows_deleted > 0:
        await callback_query.answer(
            f'Кнопка "{button_name}" была успешно удалена.'
        )
    else:
        await callback_query.answer(
            f'Кнопка "{button_name}" не найдена или уже удалена.'
        )
    await callback_query.message.edit_text(
        text='Кнопка была удалена.' if rows_deleted > 0 else 'Кнопка не найдена.',
        reply_markup=callback_query.message.reply_markup
    )


@router.message(F.text == 'статические кнопки')
async def static_button(message: Message, state: FSMContext):
    await state.set_state(FSM_DynamicButtons.working_with_buttons)
    await message.answer(
        'Работа со статическими кнопками',
        reply_markup=working_with_buttons_kb
    )
    r = await state.get_state()
    logger.debug(r)
