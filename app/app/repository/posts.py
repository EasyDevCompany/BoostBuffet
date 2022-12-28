from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload

from .base import RepositoryBase
from app.models.posts import Posts
from app.models.telegram_user import TelegramUser


class RepositoryPosts(RepositoryBase[Posts]):
    def count(self, author_id: str):
        return self._session.query(
            func.count(self._model.id)
            ).filter_by(author_id=author_id).first()

    def most_popular(self,):
        return self._session.query(
            self._model
            ).order_by(self._model.likes_amount.desc()).all()

    def most_recent(self,):
        return self._session.query(
            self._model
            ).order_by(self._model.created_at.desc()).all()

    def feed(self, followings_ids):
        return self._session.query(
            self._model
            ).options(
                joinedload(self._model.author),
            ).filter(
                self._model.author_id.in_(followings_ids),
            ).all()
