from pydantic import BaseModel

from uuid import UUID


class FollowIn(BaseModel):
    following_telegram_id: str

    class Config:
        orm_mode: True
