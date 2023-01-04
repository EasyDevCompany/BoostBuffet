from fastapi import APIRouter, Depends, UploadFile, File

from dependency_injector.wiring import inject, Provide

from typing import Optional

from app.core.containers import Container
from app.api.deps import bot_token_verification
from app.schemas.posts import PublishedPosts, DraftPosts, DefaultPosts, PostIn


router = APIRouter()


@router.post("/create_post")
@inject
async def create_post(
        data: PostIn,
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.create_post(
        user_id=token,
        post_in=data
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
        data: PostIn,
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.edit_post(
        user_id=token,
        post_url=post_url,
        post_in=data,)


@router.post("/delete_post")
@inject
async def delete_post(
        post_url: str,
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.delete_post(
        user_id=token,
        post_url=post_url,)


@router.get("/user_posts/{user_id}", response_model=list[PublishedPosts])
@inject
async def user_posts(
        user_id: str,
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.all_user_posts(
        user_id=user_id,
    )


@router.get("/my_posts")
@inject
async def my_posts(
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.my_posts(
        user_id=token,
    )


@router.get("/all_types_posts")
@inject
async def all_types_posts(
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    """
    Возвращает список постов из ленты.
    """
    return await posts_service.all_types_posts(user_id=token)


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

