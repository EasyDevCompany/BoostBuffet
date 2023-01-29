from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload

from .base import RepositoryBase
from app.models.posts import Posts
from app.models.telegram_user import TelegramUser

class RepositoryPosts(RepositoryBase[Posts]):
    def count_draft_posts(self, author_id: str):
        return self._session.query(
            func.count(self._model.id)
            ).filter_by(author_id=author_id, status=Posts.PostStatus.draft).first()

    def most_popular(self,):
        return self._session.query(
            self._model
            ).filter_by(status=Posts.PostStatus.published).order_by(self._model.likes_amount.desc())

    def most_recent(self,):
        return self._session.query(
            self._model
            ).filter_by(status=Posts.PostStatus.published).order_by(self._model.created_at.desc())

    def feed(self, followings_ids):
        return self._session.query(
            self._model
            ).options(
                joinedload(self._model.author),
            ).filter(
                self._model.author_id.in_(followings_ids),
                self._model.status == Posts.PostStatus.published
            )

    def three_last_posts(self,):
        return self._session.query(
            self._model
            ).filter_by(status=Posts.PostStatus.published).order_by(self._model.likes_amount.desc()).order_by(self._model.created_at.desc()).all()[:3]

    def most_outdated_post(self,):
        return self._session.query(
            self._model
            ).filter_by(status=Posts.PostStatus.draft).order_by(self._model.created_at.asc()).first()

    def users_leader_board(self):
        return self._session.query(
            TelegramUser.id,
            TelegramUser.telegram_id,
            TelegramUser.first_name,
            TelegramUser.surname,
            TelegramUser.username,
            func.sum(self._model.views_count),
            func.sum(self._model.likes_amount),
            func.sum(self._model.comments_count)
        ).filter(self._model.author_id == TelegramUser.id).group_by(TelegramUser.id).order_by(
            (func.sum(self._model.views_count) + 
            (func.sum(self._model.likes_amount) * 1.5) + 
            (func.sum(self._model.comments_count) * 3)).desc()
        ).all()