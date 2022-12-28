from app.db.base_class import Base
from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    DateTime,
    Enum,
    ForeignKey,
    Float,
    Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
import enum
import datetime


class FollowRelationship(Base):
    __tablename__ = 'follow_relationship'
    id = Column(
        UUID(as_uuid=True),
        default=uuid4,
        primary_key=True,
        index=True
    )
    FollowerID = Column(UUID, ForeignKey('telegramusers.id'), primary_key=True)
    FollowingID = Column(UUID, ForeignKey('telegramusers.id'), primary_key=True)

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

    followings = relationship(
        "TelegramUser",
        secondary=FollowRelationship.__tablename__,
        primaryjoin=id == FollowRelationship.FollowerID,
        secondaryjoin=id == FollowRelationship.FollowingID,
        backref="followers",
    )

    def __str__(self) -> str:
        return str(self.telegram_id) + " " + self.username if self.username else ""


