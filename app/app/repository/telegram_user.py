from app.models.telegram_user import TelegramUser, FollowRelationship
from .base import RepositoryBase


class RepositoryTelegramUser(RepositoryBase[TelegramUser]):
    pass


class RepositoryFollowRelationship(RepositoryBase[FollowRelationship]):
    pass
