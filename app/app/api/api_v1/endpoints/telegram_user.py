from fastapi import APIRouter, Depends, UploadFile, File

from dependency_injector.wiring import inject, Provide

from typing import Optional

from app.core.containers import Container

from app.api.deps import bot_token_verification


router = APIRouter()

@router.post("/subscribe")
@inject
async def subscribe(
        user_id: str,
        token = Depends(bot_token_verification),
        follow_service = Depends(Provide[Container.follow_service])):
    return await follow_service.create_follow(
        follower_id=token,
        following_id=user_id
    )
