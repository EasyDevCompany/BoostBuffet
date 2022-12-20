from aiogram import types, Dispatcher, Bot
from app.telegram_bot.loader import bot
from app.bot import dp
from app.schemas.webhook import Webhook
from aiogram.utils.exceptions import BotBlocked
from fastapi import APIRouter, Response


router = APIRouter()


@router.post("/")
async def bot_webhook(update: Webhook):
    print(update.json())
    telegram_update = types.Update(**update.dict(  ))
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    try:
        await dp.process_update(telegram_update)
    except BotBlocked:
        pass
    return Response()