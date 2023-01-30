from app.models.telegram_user import TelegramUser, FollowRelationship
from .base import RepositoryBase


class RepositoryTelegramUser(RepositoryBase[TelegramUser]):

    def get_moderators(self,):
        return self._session.query(
            self._model
            ).filter_by(role=TelegramUser.UserRole.moderator).all()


class RepositoryFollowRelationship(RepositoryBase[FollowRelationship]):
    pass
