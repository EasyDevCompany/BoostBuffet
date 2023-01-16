import requests

from app.db.base_class import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
import enum
import datetime

from app.utils.get_post_views import get_views


class Posts(Base):
    __tablename__ = "posts"

    class PostStatus(str, enum.Enum):
        draft = "draft"
        published = "published"
        not_approved= "not_approved"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    telegraph_url = Column(String)
    path = Column(String)
    title = Column(String)
    subtitle = Column(String(300))
    content = Column(String)

    status = Column(Enum(PostStatus), default=PostStatus.draft)
    likes_amount = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    author_id = Column(
        UUID(as_uuid=True),
        ForeignKey("telegramusers.id"),
    )
    author = relationship("TelegramUser")

    @property
    def views_amount(self):
        return get_views(self.path)

    @property
    def author_username(self):
        return self.author.username_link

    @property
    def post_image(self):
        req = requests.get(f"https://api.telegra.ph/getPage/{self.path}?return_content=true")
        for tag in req.json().get("result").get("content"):
            if isinstance(tag, dict) and tag.get("tag") == "img":
                return tag.get("attrs").get("src")
