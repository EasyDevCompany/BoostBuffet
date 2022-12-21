from app.models.telegram_user import TelegramUser, TelegramUserToken
from .base import RepositoryBase


class RepositoryTelegramUser(RepositoryBase[TelegramUser]):
    pass


class RepositoryTelegramUserToken(RepositoryBase[TelegramUserToken]):
    pass

