from pydantic import BaseModel

from typing import Optional


class TgProfileOut(BaseModel):
    username_link: Optional[str]
    first_name: Optional[str]
    surname: Optional[str]

    class Config:
        orm_mode = True