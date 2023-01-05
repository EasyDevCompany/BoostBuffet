from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload

from .base import RepositoryBase
from app.models.posts import Posts


class RepositoryPosts(RepositoryBase[Posts]):
    def count_draft_posts(self, author_id: str):
        return self._session.query(
            func.count(self._model.id)
            ).filter_by(author_id=author_id, status=Posts.PostStatus.draft).first()

    def most_popular(self,):
        return self._session.query(
            self._model
            ).filter_by(status=Posts.PostStatus.published).order_by(self._model.likes_amount.desc()).all()

    def most_recent(self,):
        return self._session.query(
            self._model
            ).filter_by(status=Posts.PostStatus.published).order_by(self._model.created_at.desc()).all()

    def feed(self, followings_ids):
        return self._session.query(
            self._model
            ).options(
                joinedload(self._model.author),
            ).filter(
                self._model.author_id.in_(followings_ids),
                self._model.status == Posts.PostStatus.published
            ).all()

    def most_outdated_post(self,):
        return self._session.query(
            self._model
            ).filter_by(status=Posts.PostStatus.draft).order_by(self._model.created_at.asc()).first()
