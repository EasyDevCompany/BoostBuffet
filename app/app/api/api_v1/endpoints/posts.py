from fastapi import APIRouter, Depends, UploadFile, File

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


@router.get("/user_posts/{user_id}")
@inject
async def user_posts(
        user_id: str,
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.all_posts(
        user_id=user_id,
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

