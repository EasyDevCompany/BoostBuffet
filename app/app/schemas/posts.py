from pydantic import BaseModel

from typing import Optional
from uuid import UUID

from datetime import datetime


class PostIn(BaseModel):
    title: str = "title"
    subtitle: Optional[str]
    content: str = "content"

    class Config:
        orm_mode = True


class DefaultPosts(BaseModel):
    id: UUID
    post_image: Optional[str]
    telegraph_url: str
    title: str
    subtitle: Optional[str]
    content: str
    created_at: datetime
    status: str
    author_username: str
    class Config:
        orm_mode = True

class PublishedPosts(DefaultPosts):
    views_amount: int
    likes_amount: int   
    url_to_post: Optional[str]

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


class LeaderBoard(BaseModel):
    id: UUID
    telegram_id: str
    first_name: Optional[str]
    surname: Optional[str]
    username: Optional[str]
    views: int
    reactions: int
    comments: int

    class Config:
        orm_mode = True 