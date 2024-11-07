from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


admin_panel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Посмотреть приветственное сообщение')],
        [KeyboardButton(text='Отредактировать приветственное сообщение')],
        [KeyboardButton(text='Установить количество динамических кнопок')],
        [KeyboardButton(text='статические кнопки'),
         KeyboardButton(text='динамические кнопки')]
    ],
    resize_keyboard=True)

edit_buttons_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Получить список всех кнопок')],
        [KeyboardButton(text='Удалить лишние кнопки'), KeyboardButton(text='Добавить динамическую кнопку')],
        [KeyboardButton(text='Вернуться в меню')]
    ]
)

working_with_buttons_kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text='Получить список всех кнопок')],
            [KeyboardButton(text='Удалить лишние кнопки'), KeyboardButton(text='Добавить статическую кнопку')],
            [KeyboardButton(text='Вернуться в меню')]
        ]
)
