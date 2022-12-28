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
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
import enum
import datetime


class Posts(Base):
    __tablename__ = "posts"

    class PostStatus(str, enum.Enum):
        draft = "draft"
        published = "published"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    telegraph_url = Column(String)
    path = Column(String)
    title = Column(String)
    subtitle = Column(String(300))
    content = Column(String)

    status = Column(Enum(PostStatus), default=PostStatus.draft)
    views_amount = Column(Integer, default=0)
    likes_amount = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    author_id = Column(
        UUID(as_uuid=True),
        ForeignKey("telegramusers.id"),
    )
    author = relationship("TelegramUser")
