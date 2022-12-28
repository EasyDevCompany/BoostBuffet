from fastapi import APIRouter, Response, Depends

from aiogram import types, Dispatcher, Bot
from aiogram.utils.exceptions import BotBlocked

from dependency_injector.wiring import inject, Provide

from app.core.containers import Container

from app.api.deps import bot_token_verification

from app.schemas.webhook import Webhook
from app.telegram_bot.loader import bot
from app.bot import dp


router = APIRouter()


@router.post("/")
async def bot_webhook(update: Webhook):
    telegram_update = types.Update(**update.dict(  ))
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    try:
        await dp.process_update(telegram_update)
    except BotBlocked:
        pass
    return Response()
