from fastapi import APIRouter, Depends, UploadFile, File

from dependency_injector.wiring import inject, Provide

from typing import Optional

from app.core.containers import Container
from app.api.deps import bot_token_verification
from app.schemas.posts import PublishedPosts, DraftPosts, DefaultPosts


# TODO Сделать модерацию
# TODO Схема на получение черновых постов

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


@router.post('/upload_image')
@inject
async def upload_image(
        image: UploadFile = File(...),
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.upload_image(
        user_id=token,
        image=image
    )


@router.post("/edit_post")
@inject
async def edit_post(
        post_url: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.edit_post(
        user_id=token,
        post_url=post_url,
        title=title,
        content=content
    )


@router.get("/user_posts/{user_id}", response_model=list[PublishedPosts])
@inject
async def user_posts(
        user_id: str,
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.all_user_posts(
        user_id=user_id,
    )


@router.get("/my_draft_posts")
@inject
async def my_draft_posts(
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.my_draft_posts(
        user_id=token,
    )


@router.get("/my_published_posts", response_model=list[PublishedPosts])
@inject
async def my_published_posts(
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.my_published_posts(
        user_id=token,
    )


@router.get("/popular_posts", response_model=list[PublishedPosts])
@inject
async def popular_posts(
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.popular_posts()


@router.get("/recent_posts", response_model=list[PublishedPosts])
@inject
async def recent_posts(
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.recent_posts()


@router.get("/my_feed", response_model=list[PublishedPosts])
@inject
async def my_feed(
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    """
    Возвращает список постов из ленты.
    """
    return await posts_service.my_feed(user_id=token)


# @router.post("/update_status/{post_id}")
# @inject
# async def update_status(
#         post_id: str,
#         status: str,
#         token = Depends(bot_token_verification),
#         posts_service = Depends(Provide[Container.posts_service])):
#     return await posts_service.update_status(
#         user_id=token,
#         post_id=post_id,
#         status=status
#     )

