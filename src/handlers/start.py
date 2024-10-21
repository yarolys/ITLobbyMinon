import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.enums.dice_emoji import DiceEmoji
from datetime import datetime
from src.config import logger
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from src.config import TOKEN

from src.keyboards import join2group
from src.config import BOT_ADMIN_ID

# Объект бота
bot = Bot(token=TOKEN)

# Диспетчер
dp = Dispatcher()

# Глобальная переменная для хранения времени запуска
started_at = datetime.now().strftime("%Y-%m-%d %H:%M")
# Глобальная переменная для хранения списка
mylist = [1, 2, 3]


@dp.message(Command("add_to_list"))
async def cmd_add_to_list(message: types.Message):
    mylist.append(7)
    await message.answer(f"Ваш список: {mylist}")


@dp.message(Command("info"))
async def cmd_info(message: types.Message):
    await message.answer(f"Бот запущен {started_at}")


@dp.message(F.photo)
async def get_photo(message: types.Message):
    await message.answer(f'ID фото: {message.photo[-1].file_id}')


@dp.message(Command('get_photo'))
async def get_photo(message: types.Message):
    await message.answer_photo(
        photo='AgACAgIAAxkBAANOZxEuaeAs_qj_XNhTSsFX_j0Vn-4AArHhMRsPcolIra3xaVgLQCQBAAMCAAN4AAM2BA',
        caption='это ты')


@dp.message(F.text == 'Как дела?')
async def how_are_you(message: types.Message):
    await message.answer('OK!')


# Хэндлер на команду /start
@dp.message(Command("start"))
@logger.catch
async def cmd_start(message: types.Message):
    await message.answer(f"Приветcтвую, {message.from_user.first_name}. \nТвой ID: {message.from_user.id}")


@dp.message(Command("answer"))
async def cmd_answer(message: types.Message):
    await message.reply('какашечки')


@dp.message(Command("reply"))
async def cmd_reply(message: types.Message):
    await message.reply('Это ответ с "ответом"')


@dp.message(Command("dice"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


@dp.message(Command("dice"))
async def cmd_dice_send(message: types.Message):
    await bot.send_dice(-100123123, emoji=DiceEmoji.DICE)


# Основная асинхронная функция для запуска бота
async def main():
    await dp.start_polling(bot)


# Запуск программы
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
