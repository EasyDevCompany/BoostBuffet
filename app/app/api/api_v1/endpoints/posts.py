from fastapi import APIRouter, Depends

from aiogram import types, Dispatcher, Bot
from aiogram.utils.exceptions import BotBlocked

from dependency_injector.wiring import inject, Provide

from typing import Optional

from app.core.containers import Container

from app.api.deps import bot_token_verification


router = APIRouter()

@router.post("/create_post")
@inject
async def create_post(
        title: str,
        content: str,
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.create_post(
        user_id=token,
        title=title,
        content=content
    )


@router.post("/edit_post/{post_id}")
@inject
async def edit_post(
        post_id: str,
        title: Optional[str],
        content: Optional[str],
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.edit_post(
        user_id=token,
        post_id=post_id,
        title=title,
        content=content
    )


@router.post("/update_status/{post_id}")
@inject
async def update_status(
        post_id: str,
        status: str,
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.update_status(
        user_id=token,
        post_id=post_id,
        status=status
    )

