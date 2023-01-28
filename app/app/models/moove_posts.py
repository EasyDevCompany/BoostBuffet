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


class MoovePosts(Base):
    __tablename__ = "moove_posts"

    class Category(str, enum.Enum):
        pitching = "Питчинг"
        lections = "Лекции"
        graduate_student_startups = "Стартапы выпускников"
        reading = "Читать буквы"

    class Proffesion(str, enum.Enum):
        student = "student"
        profesor = "profesor"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    title = Column(String)
    snippet = Column(String)
    post_url = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    category = Column(Enum(Category), nullable=True)
