from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from dependency_injector.wiring import inject, Provide

from app.core.containers import Container
from app.api.deps import bot_token_verification, commit_and_close_session

from app.schemas.moove_posts import MoovePost


router = APIRouter()

@router.post("/upload_moove_post")
@inject
@commit_and_close_session
async def upload_moove_post(
        url: str,
        category: str,
        token = Depends(bot_token_verification),
        moove_service = Depends(Provide[Container.moove_posts_service])):
    return await moove_service.upload_post_url(url, category)


@router.post("/all_moove_posts", response_model=Page[MoovePost])
@inject
@commit_and_close_session
async def all_moove_posts(
        category: str,
        token = Depends(bot_token_verification),
        moove_service = Depends(Provide[Container.moove_posts_service])):
    return await moove_service.all_posts(category=category)


@router.post("/all_categories")
@inject
@commit_and_close_session
async def all_categories(
        token = Depends(bot_token_verification),
        moove_service = Depends(Provide[Container.moove_posts_service])):
    return await moove_service.all_cateogories()
