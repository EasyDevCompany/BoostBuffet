from fastapi import APIRouter, Depends

from dependency_injector.wiring import inject, Provide

from app.core.containers import Container
from app.api.deps import bot_token_verification


router = APIRouter()

@router.post("/upload_moove_post")
@inject
async def upload_moove_post(
        url: str,
        category: str,
        token = Depends(bot_token_verification),
        moove_service = Depends(Provide[Container.moove_posts_service])):
    return await moove_service.upload_post_url(url, category)


@router.post("/all_moove_posts")
@inject
async def all_moove_posts(
        token = Depends(bot_token_verification),
        moove_service = Depends(Provide[Container.moove_posts_service])):
    return await moove_service.all_posts()


@router.post("/all_categories")
@inject
async def all_categories(
        token = Depends(bot_token_verification),
        moove_service = Depends(Provide[Container.moove_posts_service])):
    return await moove_service.all_cateogories()
