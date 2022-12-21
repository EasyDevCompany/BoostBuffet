from app.db.base_class import Base
from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    DateTime,
    Enum,
    ForeignKey,
    Float
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from uuid import uuid4
import enum
import datetime


class TelegramUser(Base):
    __tablename__ = "telegramusers"

    class UserType(enum.Enum):
        active = "active"
        blocked = "blocked"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    telegram_id = Column(BigInteger, unique=True, index=True)
    username = Column(String, nullable=True)
    registration_date = Column(DateTime, default=datetime.datetime.utcnow)
    type = Column(Enum(UserType))
    raiting = Column(Float(precision=1), default=0)
    likes_amount = Column(Integer, default=0)

    def __str__(self) -> str:
        return str(self.telegram_id) + " " + self.username if self.username else ""


class TelegramUserToken(Base):
    __tablename__ = "telegramuserstokens"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("telegramusers.id"), unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
