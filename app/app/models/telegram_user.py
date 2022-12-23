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

    class UserType(str, enum.Enum):
        active = "active"
        blocked = "blocked"

    class UserRole(str, enum.Enum):
        user = "user"
        moderator = "moderator"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    telegram_id = Column(BigInteger, unique=True, index=True)

    telegraph_access_token = Column(String)
    username = Column(String, nullable=True)
    registration_date = Column(DateTime, default=datetime.datetime.utcnow)
    type = Column(Enum(UserType), default=UserType.active)
    role = Column(Enum(UserRole), default=UserRole.user)
    raiting = Column(Float(precision=1), default=0)
    likes_amount = Column(Integer, default=0)

    def __str__(self) -> str:
        return str(self.telegram_id) + " " + self.username if self.username else ""
