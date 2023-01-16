import enum

from sqlalchemy import (
    Enum,
    Column,
    String,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from uuid import uuid4

from app.db.base_class import Base

from app.core.config import settings


class Cards(Base):
    __tablename__ = "cards"

    class ApprovalStatus(str, enum.Enum):
        approved = "approved"
        not_approved = "not_approved"
        draft = "draft"

    class CardRole(str, enum.Enum):
        beginner = "Носильщик кофе"
        adept = "Идейный вдохновитель"
        master = "Гроза инвесторов"
        sage = "Раундовый тяжеловес"
        legend = "Покоритель единорогов"

    class Tag(str, enum.Enum):
        fintech = "Финтех"
        design = "Дизайн"

    class Proffesion(str, enum.Enum):
        student = "student"
        profesor = "profesor"

    class ChatOpen(str, enum.Enum):
        available = "available"
        not_available = "not_available"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)

    username = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    raiting = Column(Integer, default=0)
    description = Column(String(150), nullable=True)

    aprroval_status = Column(Enum(ApprovalStatus), default=ApprovalStatus.draft)
    role = Column(Enum(CardRole), default=CardRole.beginner)
    first_tag = Column(Enum(Tag), nullable=False)
    second_tag = Column(Enum(Tag), nullable=False)
    proffesion = Column(Enum(Proffesion), default=Proffesion.student)
    chat_open = Column(Enum(ChatOpen), default=ChatOpen.available)

    author_id = Column(
        UUID(as_uuid=True),
        ForeignKey("telegramusers.id"),
    )
    author = relationship("TelegramUser")

    @property
    def card_profile_img(self):
        return f"{settings.SERVER_IP}/image/{self.author.telegram_id}/card_image.png"

    @property
    def author_username(self):
        return f"@{self.username}"

# TODO Решить архитектурный вопрос с тэгами