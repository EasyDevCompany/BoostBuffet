from pydantic import BaseModel

from typing import Optional
from uuid import UUID

from datetime import datetime


class PostIn(BaseModel):
    title: str
    subtitle: str
    content: str

    class Config:
        orm_mode = True


class DefaultPosts(BaseModel):
    post_image: Optional[str]
    telegraph_url: str
    title: str
    content: str
    created_at: datetime
    status: str
    author_id: UUID

    class Config:
        orm_mode = True

class PublishedPosts(DefaultPosts):
    views_amount: int
    likes_amount: int

    class Config:
        orm_mode = True


class DraftPosts(BaseModel):
    posts: list[PublishedPosts]
    draft_count: int

    class Config:
        orm_mode = True


class MyPosts(BaseModel):
    published: list[DefaultPosts]
    not_approved: list[DefaultPosts]
    draft: DraftPosts
    class Config:
        orm_mode = True


class AllPosts(BaseModel):
    popular: list[DefaultPosts]
    recent: list[DefaultPosts]
    my_feed: list[DefaultPosts]

    class Config:
        orm_mode = True
