from aiogram import types
from uuid import uuid4

from dependency_injector.wiring import inject, Provide

from aiogram.dispatcher.filters.builtin import CommandStart

from app.telegram_bot.loader import bot, dp

from app.core.containers import Container, SyncSession, TelegramUser
from app.db.session import scope
from app.telegram_bot import const
from app.telegram_bot.keyboards.start_menu import get_menu_button, get_menu_web_app


@dp.message_handler(CommandStart(), state="*")
@inject
async def process_start_command(
        message: types.Message,
        rep_telegram_user = Provide[Container.repository_telegram_user]):
    """Выполняется при команде /start."""
    scope.set(str(uuid4))
    user = rep_telegram_user.get(telegram_id=int(message.from_user.id))
    if not user:
        user = rep_telegram_user.create(
            obj_in={
                "telegram_id": message.from_user.id,
                "username": message.from_user.username,
                "type": TelegramUser.UserType.active,
                "raiting": 0
            }, commit=True)
        await bot.send_message(message.from_user.id, const.START_TEXT, reply_markup=get_menu_button())
    else:
        await bot.send_message(message.from_user.id, f"{const.START_TEXT} {user.username}", reply_markup=get_menu_button())
        await bot.set_chat_menu_button(
            chat_id=message.chat.id,
            menu_button=get_menu_web_app()
        )
