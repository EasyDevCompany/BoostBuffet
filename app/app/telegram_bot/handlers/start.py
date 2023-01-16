from pathlib import Path

from aiogram import types
from uuid import uuid4

from dependency_injector.wiring import inject, Provide

from aiogram.dispatcher.filters.builtin import CommandStart

from app.telegram_bot.loader import bot, dp

from app.core.containers import Container, TelegramUser
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
    await download_profile_picture(tg_user_id=message.from_user.id, telegram_id=message.from_user.id)
    if not user:
        res = Container.telegraph.create_account(short_name=message.from_user.username)
        user = rep_telegram_user.create(
            obj_in={
                "telegram_id": message.from_user.id,
                "username": message.from_user.username,
                "first_name": message.from_user.first_name,
                "surname": message.from_user.last_name,
                "telegraph_access_token": res.get("access_token"),
                "type": TelegramUser.UserType.active,
                "raiting": 0
            }, commit=True)
        await create_folder_for_user_image(telegram_id=message.from_user.id)

        await bot.send_message(message.from_user.id, const.START_TEXT, reply_markup=get_menu_button())
    else:
        await bot.send_message(message.from_user.id, f"{const.START_TEXT} {user.username}", reply_markup=get_menu_button())
        await bot.set_chat_menu_button(
            chat_id=message.chat.id,
            menu_button=get_menu_web_app()
        )


async def create_folder_for_user_image(telegram_id):
    post_image_dir = await get_image_dir() / str(telegram_id)
    post_image_dir.mkdir(parents=True, exist_ok=True)


async def get_image_dir():
    current_file = Path(__file__)
    current_file_dir = current_file.parent
    project_root = current_file_dir.parent.parent.parent
    return project_root / "image"


async def download_profile_picture(tg_user_id: str, telegram_id: str):
    photo = await bot.get_user_profile_photos(tg_user_id)
    file_id = photo.photos[0][0].file_id
    profile_image_dir = await get_image_dir() / f"{telegram_id}" / "profile_picture.png"
    card_profile_image_dir = await get_image_dir() / f"{telegram_id}" / "card_image.png"
    await bot.download_file_by_id(file_id=file_id, destination=profile_image_dir)
    await bot.download_file_by_id(file_id=file_id, destination=card_profile_image_dir)
