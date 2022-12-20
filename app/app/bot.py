from aiogram import executor
from app.core.containers import Container
from app.telegram_bot.loader import dp
from app.telegram_bot import handlers

container = Container()
container.wire(packages=[handlers])
container.init_resources()