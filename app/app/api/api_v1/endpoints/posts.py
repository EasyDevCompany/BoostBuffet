from fastapi import APIRouter, Depends, UploadFile, File

from dependency_injector.wiring import inject, Provide

from typing import Optional


from app.core.containers import Container
from app.api.deps import bot_token_verification, commit_and_close_session
from app.schemas.posts import PublishedPosts, PostIn, MyPosts, AllPosts, DefaultPosts, LeaderBoard

from fastapi_pagination import Page


router = APIRouter()


@router.post("/create_post", response_model=DefaultPosts)
@inject
@commit_and_close_session
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
@commit_and_close_session
async def upload_image(
        image: UploadFile = File(...),
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.upload_image(
        user_id=token,
        image=image
    )


@router.post('/upload_video')
@inject
@commit_and_close_session
async def upload_video(
        video: UploadFile = File(...),
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.upload_video(
        user_id=token,
        video=video
    )


@router.post("/edit_post")
@inject
@commit_and_close_session
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
@commit_and_close_session
async def delete_post(
        post_url: str,
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.delete_post(
        user_id=token,
        post_url=post_url,)


@router.get("/post/{post_id}", response_model=PublishedPosts)
@inject
@commit_and_close_session
async def post(
        post_id: str,
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.get_post(
        post_id=post_id,
    )


@router.get("/user_posts/{user_id}", response_model=list[PublishedPosts])
@inject
@commit_and_close_session
async def user_posts(
        user_id: str,
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.all_user_posts(
        user_id=user_id,
    )


@router.get("/my_posts", response_model=MyPosts)
@inject
@commit_and_close_session
async def my_posts(
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.my_posts(
        user_id=token,
    )


@router.get("/all_types_posts", response_model=AllPosts)
@inject
@commit_and_close_session
async def all_types_posts(
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    """
    Возвращает список постов из ленты.
    """
    return await posts_service.all_types_posts(user_id=token)


@router.get("/popular_posts", response_model=Page[PublishedPosts])
@inject
@commit_and_close_session
async def popular_posts(
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.popular_posts()


@router.get("/recent_posts", response_model=Page[PublishedPosts])
@inject
@commit_and_close_session
async def recent_posts(
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.recent_posts()


@router.get("/my_feed", response_model=Page[PublishedPosts])
@inject
@commit_and_close_session
async def my_feed(
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.my_feed(user_id=token)


@router.get("/three_last_posts", response_model=list[PublishedPosts])
@inject
@commit_and_close_session
async def three_last_posts(
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    """
    Возвращает 3 поста для блока "есть что почитать".
    """
    return await posts_service.three_last_posts()


@router.get("/draft_post", response_model=DefaultPosts)
@inject
@commit_and_close_session
async def get_draft_post(
        post_id: str,
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])):
    return await posts_service.get_draft_post(user_id=token, post_id=post_id)


@router.get("/draft_posts", response_model=list[DefaultPosts])
@inject
@commit_and_close_session
async def list_draft_post(
    token = Depends(bot_token_verification),
    posts_service = Depends(Provide[Container.posts_service])
):
    return await posts_service.list_draft_posts(user_id=token)

@router.get("/leader_board", response_model=list[LeaderBoard])
@inject
@commit_and_close_session
async def get_leader_board(
        token = Depends(bot_token_verification),
        posts_service = Depends(Provide[Container.posts_service])
):
    return await posts_service.leader_board()
