from fastapi import APIRouter, Depends

from dependency_injector.wiring import inject, Provide

from app.core.containers import Container

from app.api.deps import bot_token_verification

from app.schemas.follow_relation import FollowIn
from app.schemas.telegram_user import TgProfileOut


router = APIRouter()


@router.get("/my_profile", response_model=TgProfileOut)
@inject
async def my_profile(
        token = Depends(bot_token_verification),
        telegram_service = Depends(Provide[Container.telegram_user_service])):
    return await telegram_service.my_profile(user_id=token)


@router.post("/subscribe")
@inject
async def subscribe(
        follow_in: FollowIn,
        token = Depends(bot_token_verification),
        follow_service = Depends(Provide[Container.follow_service])):
    return await follow_service.create_follow(
        follower_id=token,
        follow_in=follow_in
    )
