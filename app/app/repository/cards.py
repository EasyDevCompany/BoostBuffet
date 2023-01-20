from sqlalchemy import or_

from .base import RepositoryBase

from app.models.cards import Cards

from app.schemas.cards import TagIn


class RepositoryCards(RepositoryBase[Cards]):

    def all_cards(self, tag_in: TagIn):
        tags = [
            "Финтех",
            "Дизайн",
            "Adobe",
            "Figma",
            "Tilda",
            "Java",
            "Script",
            "Python",
            "СС",
            "PHP",
            "Google Analytics",
            "Яндекс Метрика",
            "Тайм-менеджмент"
            "Переговоры",
            "Лидерство",
            "Менторство",
            "Трекинг",
            "ВШЭ",
            "Плеханова",
            "МГУ",
            "МФТИ",
            "МИФИ",
            "РУДН",
            "МГИМО",
            "РАНХиГС",
            "СПБГУ",
            "СПБГТУ",
            "НГУ",
            "ННГУ",
            "ТПУ",
            "Project_Manager",
            "Product Manager",
            "Стартапер",
            "Data Science",
            "Маркетолог",
            "Разработчик",
            "Аналитик",
            "Инженер",
            "UX/UI"
        ]
        query = self._session.query(
            self._model
            ).filter_by(aprroval_status=Cards.ApprovalStatus.approved)
        # Есть 2^3 = 8 вероятных возможностей для комбинацией тегов 
        # Здесь описаны все 8. 000, 100, 010, 001, 110, 101, 011, 111
        # Где first_tag, second_tag, third_tag расположены соответственно порядку цифр

        # 111
        if tag_in.first_tag != "None" and tag_in.second_tag != "None" and tag_in.third_tag != "None":
            query = query.filter(
                or_(
                    self._model.first_tag.in_((tag_in.first_tag , tag_in.second_tag, tag_in.third_tag)),
                    self._model.second_tag.in_((tag_in.first_tag, tag_in.second_tag, tag_in.third_tag)),
                    self._model.third_tag.in_((tag_in.first_tag, tag_in.second_tag, tag_in.third_tag)),
                )
            )
        # 100
        elif tag_in.first_tag != "None" and tag_in.second_tag == "None" and tag_in.third_tag == "None":
            query = query.filter(
                or_(
                    self._model.first_tag == tag_in.first_tag,
                    self._model.second_tag == tag_in.first_tag,
                    self._model.third_tag == tag_in.first_tag
                )
            )
        # 010
        elif tag_in.second_tag != "None" and tag_in.first_tag == "None" and tag_in.third_tag == "None":
            query = query.filter(
                or_(
                    self._model.first_tag == tag_in.second_tag,
                    self._model.second_tag == tag_in.second_tag,
                    self._model.third_tag == tag_in.second_tag
                )
            )
        # 001
        elif tag_in.first_tag == "None" and tag_in.second_tag == "None" and tag_in.third_tag != "None":
            query = query.filter(
                or_(
                    self._model.first_tag == tag_in.third_tag,
                    self._model.second_tag == tag_in.third_tag,
                    self._model.third_tag == tag_in.third_tag
                )
            )
        # 110
        elif tag_in.first_tag != "None" and tag_in.second_tag != "None" and tag_in.third_tag == "None":
            query = query.filter(
                or_(
                    self._model.first_tag.in_((tag_in.first_tag , tag_in.second_tag)),
                    self._model.second_tag.in_((tag_in.first_tag, tag_in.second_tag)),
                    self._model.third.in_((tag_in.first_tag, tag_in.second_tag)),
                )
            )
        # 101
        elif tag_in.first_tag != "None" and tag_in.third_tag != "None" and tag_in.second_tag == "None":
            query = query.filter(
                or_(
                    self._model.first_tag.in_((tag_in.first_tag , tag_in.second_tag)),
                    self._model.second_tag.in_((tag_in.first_tag , tag_in.second_tag)),
                    self._model.third_tag.in_((tag_in.first_tag, tag_in.third_tag)),
                )
            )
        # 011
        elif tag_in.first_tag == "None" and tag_in.second_tag != "None" and tag_in.third_tag != "None":
            query = query.filter(
                or_(
                    self._model.first_tag.in_((tag_in.second_tag , tag_in.third_tag)),
                    self._model.second_tag.in_((tag_in.second_tag , tag_in.third_tag)),
                    self._model.third_tag.in_((tag_in.second_tag, tag_in.third_tag)),
                )
            )
        # 000
        return query
    
    def three_last_cards(self,):
        return self._session.query(
            self._model
            ).filter_by(
                aprroval_status=Cards.ApprovalStatus.approved
                ).order_by(self._model.raiting.desc()).all()[:3]