from pydantic import BaseModel

from uuid import UUID

from datetime import datetime

from app.models.posts import Posts


class PostIn(BaseModel):
    title: str
    subtitle: str
    content: str

    class Config:
        orm_mode = True


class DefaultPosts(BaseModel):
    telegraph_url: str
    title: str
    content: str
    created_at: datetime
    status: str
    author_id: UUID

class PublishedPosts(DefaultPosts):
    views_amount: int
    likes_amount: int

    class Config:
        orm_mode = True


class DraftPosts(BaseModel):
    # __root__ = Posts
    posts: list[DefaultPosts]
    draft_count: int

    class Config:
        orm_mode = True
