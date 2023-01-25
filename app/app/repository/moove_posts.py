from app.models.moove_posts import MoovePosts
from .base import RepositoryBase


class RepositoryMoovePosts(RepositoryBase[MoovePosts]):

    def filter_category(self, category):
        return self._session.query(self._model).filter_by(category=category)
