from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File

from dependency_injector.wiring import inject, Provide

from app.core.containers import Container
from app.api.deps import bot_token_verification

from app.schemas.cards import TagIn, CardsOut, CardIn, DefaultCard, UpdateCardIn

from fastapi_pagination import Page



router = APIRouter()

@router.post("/all_cards", response_model=Page[DefaultCard])
@inject
async def all_cards(
        tag_in: TagIn,
        token = Depends(bot_token_verification),
        cards_service = Depends(Provide[Container.cards_service]),):
    return await cards_service.all_cards(tag_in=tag_in)


@router.post("/create_card", response_model=DefaultCard)
@inject
async def create_card(
        card_in: CardIn,
        token = Depends(bot_token_verification),
        cards_service = Depends(Provide[Container.cards_service]),):
    return await cards_service.create_card(user_id=token, card_in=card_in)


@router.post('/upload_image')
@inject
async def upload_image(
        image: UploadFile = File(...),
        token = Depends(bot_token_verification),
        cards_service = Depends(Provide[Container.cards_service]),):
    return await cards_service.upload_image(
        user_id=token,
        image=image
    )


@router.post("/update_card")
@inject
async def update_card(
        update_card_in: UpdateCardIn,
        token = Depends(bot_token_verification),
        cards_service = Depends(Provide[Container.cards_service]),):
    return await cards_service.update_card(update_card_in=update_card_in, user_id=token)


@router.get("/user_card/{username}", response_model=Optional[DefaultCard])
@inject
async def user_card(
        username: str,
        token = Depends(bot_token_verification),
        cards_service = Depends(Provide[Container.cards_service]),):
    return await cards_service.user_card(username=username)


@router.get("/my_card", response_model=Optional[DefaultCard])
@inject
async def my_card(
        token = Depends(bot_token_verification),
        cards_service = Depends(Provide[Container.cards_service]),):
    return await cards_service.my_card(user_id=token)


@router.get("/tags")
@inject
async def tags(
        token = Depends(bot_token_verification),
        cards_service = Depends(Provide[Container.cards_service]),):
    return await cards_service.all_tags()


@router.post("/send_message")
@inject
async def send_message(
        username: str,
        text: str,
        token = Depends(bot_token_verification),
        cards_service = Depends(Provide[Container.cards_service]),):
    return await cards_service.send_message(username=username, text=text)


@router.post("/add_raiting")
@inject
async def add_raiting(
        raiting: int,
        user_id: str,
        token = Depends(bot_token_verification),
        cards_service = Depends(Provide[Container.cards_service]),):
    return await cards_service.add_raiting(user_id=user_id, moderator_id=token, raiting=raiting)
