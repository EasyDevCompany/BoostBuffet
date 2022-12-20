from app.telegram_bot.loader import bot, dp
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart


@dp.message_handler(CommandStart(), state="*")
async def process_start_command(message: types.Message):
    await message.reply("Hello world")