from app.models.moove_posts import MoovePosts
from .base import RepositoryBase


class RepositoryMoovePosts(RepositoryBase[MoovePosts]):

    def all_posts(self):
        return self._session.query(self._model)

    def filter_category(self, category):
        return self._session.query(self._model).filter_by(category=category)

    def three_last_mooove_posts(self):
        return self._session.query(self._model).order_by(self._model.created_at.desc()).all()
