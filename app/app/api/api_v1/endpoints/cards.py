from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File

from dependency_injector.wiring import inject, Provide

from app.core.containers import Container
from app.api.deps import bot_token_verification, commit_and_close_session

from app.schemas.cards import TagIn, CardsOut, CardIn, DefaultCard, UpdateCardIn

from fastapi_pagination import Page



router = APIRouter()

@router.post("/all_cards", response_model=Page[DefaultCard])
@inject
@commit_and_close_session
async def all_cards(
        tag_in: TagIn,
        token = Depends(bot_token_verification),
        cards_service = Depends(Provide[Container.cards_service]),):
    return await cards_service.all_cards(tag_in=tag_in)


@router.post("/create_card", response_model=DefaultCard)
@inject
@commit_and_close_session
async def create_card(
        card_in: CardIn,
        token = Depends(bot_token_verification),
        cards_service = Depends(Provide[Container.cards_service]),):
    return await cards_service.create_card(user_id=token, card_in=card_in)


@router.post('/upload_image')
@inject
@commit_and_close_session
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
@commit_and_close_session
async def update_card(
        update_card_in: UpdateCardIn,
        token = Depends(bot_token_verification),
        cards_service = Depends(Provide[Container.cards_service]),):
    return await cards_service.update_card(update_card_in=update_card_in, user_id=token)


@router.get("/user_card/{username}", response_model=Optional[DefaultCard])
@inject
@commit_and_close_session
async def user_card(
        username: str,
        token = Depends(bot_token_verification),
        cards_service = Depends(Provide[Container.cards_service]),):
    return await cards_service.user_card(username=username)


@router.get("/my_card", response_model=Optional[DefaultCard])
@inject
@commit_and_close_session
async def my_card(
        token = Depends(bot_token_verification),
        cards_service = Depends(Provide[Container.cards_service]),):
    return await cards_service.my_card(user_id=token)


@router.get("/three_last_cards", response_model=list[DefaultCard])
@inject
@commit_and_close_session
async def three_last_cards(
        token = Depends(bot_token_verification),
        cards_service = Depends(Provide[Container.cards_service]),):
    return await cards_service.three_last_cards()


@router.get("/tags")
@inject
@commit_and_close_session
async def tags(
        token = Depends(bot_token_verification),
        cards_service = Depends(Provide[Container.cards_service]),):
    return await cards_service.all_tags()


@router.post("/send_message")
@inject
@commit_and_close_session
async def send_message(
        username: str,
        text: str,
        token = Depends(bot_token_verification),
        cards_service = Depends(Provide[Container.cards_service]),):
    return await cards_service.send_message(username=username, text=text)


@router.post("/add_raiting")
@inject
@commit_and_close_session
async def add_raiting(
        raiting: int,
        user_id: str,
        token = Depends(bot_token_verification),
        cards_service = Depends(Provide[Container.cards_service]),):
    return await cards_service.add_raiting(user_id=user_id, moderator_id=token, raiting=raiting)
