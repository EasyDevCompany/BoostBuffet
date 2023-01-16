from sqlalchemy import or_

from .base import RepositoryBase
from app.models.cards import Cards


class RepositoryCards(RepositoryBase[Cards]):

    def all_cards(self, first_tag: str, second_tag: str):
        query = self._session.query(
            self._model
            ).filter_by(aprroval_status=Cards.ApprovalStatus.approved)
        if first_tag != "None" and second_tag != "None":
            query = query.filter(
                or_(
                    self._model.first_tag.in_((first_tag, second_tag)),
                    self._model.second_tag.in_((first_tag, second_tag))
                )
            )
        elif first_tag != "None" and second_tag == "None":
            query = query.filter(self._model.first_tag == first_tag)
        elif second_tag != "None" and first_tag == "None":
            query = query.filter(self._model.second_tag == second_tag)
        return query.all()