from pathlib import Path

from typing import Optional

from fastapi.responses import JSONResponse

from app.core.config import settings

from app.repository.cards import RepositoryCards
from app.repository.telegram_user import RepositoryTelegramUser

from app.models.cards import Cards

from app.telegram_bot.loader import bot

from app.schemas.cards import CardIn, UpdateCardIn, TagIn
from fastapi_pagination.ext.sqlalchemy import paginate

from app.logs.logger_config import catch_logs

class CardsService:

    def __init__(
            self,
            repository_cards: RepositoryCards,
            repository_telegram_user: RepositoryTelegramUser,) -> None:

        self._repository_cards = repository_cards
        self._repository_telegram_user = repository_telegram_user

    @catch_logs
    async def all_cards(
            self,
            tag_in: TagIn,
            user_id: str):

        return paginate(self._repository_cards.all_cards(tag_in=tag_in, user_id=user_id))

    @catch_logs
    async def create_card(self, user_id: str, card_in: CardIn):
        user = self._repository_telegram_user.get(id=user_id)
        card = self._repository_cards.get(author_id=user_id)
        if card:
            return JSONResponse(content={"error_msg": "У вас уже существует карточка"}, status_code=403)
        if not user.username:
            return JSONResponse(content={"error_msg": "У вас отсутствует username"}, status_code=403)
        return self._repository_cards.create(
            obj_in={
                "username": user.username,
                "first_name": user.first_name,
                "surname": user.surname,
                "description": card_in.description or user.description,
                "bio": card_in.bio,
                "first_tag": card_in.first_tag,
                "second_tag": card_in.second_tag,
                "third_tag": card_in.third_tag,
                "author": user,
                "chat_open": card_in.chat_available,
                "aprroval_status": "draft",
            },
            commit=True)

    @catch_logs
    async def update_card(self, update_card_in: UpdateCardIn, user_id: str):
        card = self._repository_cards.get(author_id=user_id)
        if update_card_in.first_tag == "Null":
            first_tag = None
        else:
            first_tag = card.first_tag
        if update_card_in.second_tag == "Null":
            second_tag = None
        else:
            second_tag = card.second_tag
        if update_card_in.third_tag == "Null":
            third_tag = None
        else:
            third_tag = card.third_tag
        return self._repository_cards.update(
            db_obj=card,
            obj_in={
                "description": update_card_in.description or card.description,
                "bio": update_card_in.bio or card.bio,
                "chat_open": update_card_in.chat_open or card.chat_open,
                "first_tag": first_tag,
                "second_tag": second_tag,
                "third_tag": third_tag
            }
        )

    @catch_logs
    async def upload_image(self, user_id, image):
        user = self._repository_telegram_user.get(id=user_id)

        current_file = Path(__file__)
        current_file_dir = current_file.parent
        project_root = current_file_dir.parent.parent / f"image/{user.telegram_id}"
        project_root_absolute = project_root.resolve()
        static_root_absolute = project_root_absolute / f"card_image.png"
        file_location = static_root_absolute
        with open(file_location, "wb+") as file_object:
            image.filename = f"card_image.png"
            file_object.write(image.file.read())

        represantation = {"img_path": f"/image/{user.telegram_id}/{image.filename}"}
        return JSONResponse(status_code=200, content=represantation)

    @catch_logs
    async def user_card(self, username):
        user = self._repository_telegram_user.get(username=username)
        if not user:
            return None
        return self._repository_cards.get(author_id=user.id)

    @catch_logs
    async def my_card(self, user_id):
        return self._repository_cards.get(author_id=user_id)

    @catch_logs
    async def three_last_cards(self):
        return self._repository_cards.three_last_cards()

    @catch_logs
    async def send_message(self, username: str, text: str):
        user = self._repository_telegram_user.get(username=username)
        await bot.send_message(user.telegram_id, text=text)
        return JSONResponse(content="Сообщение было отправлено", status_code=200)

    @catch_logs
    async def add_raiting(self, user_id: str, moderator_id: str, raiting: int):
        moderator_user = self._repository_telegram_user.get(telegram_id=moderator_id)
        user = self._repository_telegram_user.get(id=user_id)
        if moderator_user.role != "moderator":
            return JSONResponse(content="У вас нет прав на обновление рейтинга", status_code=403)
        card = self._repository_cards.get(author_id=user.id)
        if not card:
            return JSONResponse(content={"error_msg": "У вас нет карточки"}, status_code=403)
        self._repository_cards.update(
            db_obj=card,
            obj_in={
                "raiting": card.raiting + raiting
            }
        )
        return JSONResponse(content="Рейтинг был обновлён", status_code=200)

    @catch_logs
    async def all_tags(self,):
        tags = [
            "Финтех",
            "Дизайн",
            "Adobe",
            "Figma",
            "Tilda",
            "Java",
            "Script",
            "Python",
            "СС++",
            "PHP",
            "Google Analytics",
            "Яндекс Метрика",
            "Тайм-менеджмент",
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
        return JSONResponse(status_code=200, content=tags)
