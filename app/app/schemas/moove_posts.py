from pydantic import BaseModel

from typing import Optional
from uuid import UUID

from datetime import datetime


class MoovePost(BaseModel):
    id: UUID
    title: str
    snippet: str
    post_url: str
    image_url: str
    created_at: datetime
    category: str

    class Config:
        orm_mode = True
