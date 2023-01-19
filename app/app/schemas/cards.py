from typing import Optional

from pydantic import BaseModel, root_validator

from uuid import UUID


class TagIn(BaseModel):
    first_tag: Optional[str] = "None"
    second_tag: Optional[str] = "None"
    third_tag: Optional[str] = "None"


class DefaultCard(BaseModel):
    id: UUID
    author_username: str
    first_name: Optional[str]
    surname: Optional[str]
    raiting: str
    description: Optional[str]
    aprroval_status: str
    role: str
    proffesion: str
    first_tag: str
    second_tag: str
    third_tag: str
    chat_open: str
    card_profile_img: str

    class Config:
        orm_mode = True


class CardsOut(BaseModel):
    cards: list[DefaultCard]

    class Config:
        orm_mode = True


class CardIn(BaseModel):
    description: str
    first_tag: str
    second_tag: str
    third_tag: str
    chat_available: str = "available"

    @root_validator
    @classmethod
    def validate_tags_not_equal(cls, field_value):
        if len(set((field_value["first_tag"], field_value["second_tag"], field_value["third_tag"]))) <3:
            raise ValueError("Вы не можете выбрать одинаковые тэги")
        return field_value


class UpdateCardIn(BaseModel):
    chat_open: Optional[str]
    description: Optional[str]
    first_tag: Optional[str]
    second_tag: Optional[str]
    third_tag: Optional[str]
