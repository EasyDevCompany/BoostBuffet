from aiogram import types
from app.core.config import settings


def get_menu_button():
    web_app = types.WebAppInfo(url=f"{settings.WEBAPP_URL}")
    web_app_inline_keyboard = types.InlineKeyboardButton(
        text="Начать",
        web_app=web_app
    )
    return types.InlineKeyboardMarkup().add(web_app_inline_keyboard)


def get_menu_web_app():
    web_app = types.WebAppInfo(url=f"{settings.WEBAPP_URL}")
    return types.MenuButtonWebApp(text="Начать", web_app=web_app)
