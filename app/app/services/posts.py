from pathlib import Path
from random import randint

from fastapi.responses import JSONResponse

from fastapi_pagination.ext.sqlalchemy import paginate

from telegraph import Telegraph
from telegraph.exceptions import TelegraphException

from app.core.config import settings

from app.models.posts import Posts

from app.repository.posts import RepositoryPosts, Posts
from app.repository.telegram_user import RepositoryTelegramUser

from app.telegram_bot.loader import bot

from app.schemas.posts import PostIn

from app.logs.logger_config import catch_logs

from loguru import logger

from app.telegram_bot.keyboards.moderator_keyboards import get_post_approve_buttons, get_card_approve_buttons


class PostsService:

    def __init__(
            self,
            repository_telegram_user: RepositoryTelegramUser,
            repository_posts: RepositoryPosts,) -> None:

        self._repository_telegram_user = repository_telegram_user
        self._repository_posts = repository_posts

    @catch_logs
    async def create_post(self, user_id: str, post_in: PostIn):
        user = self._repository_telegram_user.get(id=user_id)
        telegraph = Telegraph(user.telegraph_access_token)
        try:
            author_url = 'https://t.me/boostbuffet'
            post = telegraph.create_page(
                post_in.title or '',
                author_url=author_url,
                author_name="MOOVE Медиахаб boostbuffettest",
                html_content=post_in.content + f"<br><br>Автор: <a href='https://t.me/{user.username}'>@{user.username}</a>"

            )
            post = self._repository_posts.create(
                obj_in={
                    "telegraph_url": post.get("url"),
                    "path": post.get("path"),
                    "title": post.get("title"),
                    "content": post_in.content,
                    "subtitle": post_in.subtitle or None,
                    "status": Posts.PostStatus.draft,
                    "author": user,
                }, commit=True)

            await bot.send_message(
                user.telegram_id,
                "Ваш пост отправлен на модерацию.",
                parse_mode='HTML'
            )
            moderators = self._repository_telegram_user.get_moderators()
            for moderator in moderators:
                await bot.send_message(
                    moderator.telegram_id,
                    f'<b>{post.title}</b> \n{post.subtitle} \nАвтор: @{post.author.username} \n{post.telegraph_url}',
                    reply_markup=get_post_approve_buttons(post_id=post.id)
                )

        except TelegraphException as er:
            if str(er) == "TITLE_TOO_LONG":
                return JSONResponse(status_code=400, content={"error": "Слишком длинный заголовок"})
            if str(er) == "ACCESS_TOKEN_INVALID":
                return JSONResponse(status_code=400, content={"error": "Неверный токен!"})
            return JSONResponse(status_code=400, content={"error": f"{er}"})

        return post

    @catch_logs
    async def edit_post(
            self,
            user_id: str,
            post_url: str,
            post_in: PostIn,):
        user = self._repository_telegram_user.get(id=user_id)
        post = self._repository_posts.get(telegraph_url=post_url)
        if post.author != user:
            return JSONResponse(status_code=403, content={"error": "Вы не являетесь автором поста"})

        telegraph = Telegraph(user.telegraph_access_token)
        try:
            telegraph.edit_page(
                path=post.path,
                title=post_in.title or post.title,
                html_content=post_in.content or post.content
            )
            self._repository_posts.update(
                db_obj=post,
                obj_in={
                    "title": post_in.title or post.title,
                    "content": post_in.content or post.content,
                    "status": Posts.PostStatus.draft
                }
            )
            await bot.send_message(
                user.telegram_id,
                f'Вы отредактировали пост <a href="{post.telegraph_url}">{post.title}</a> <b>{post.subtitle}</b>',
                parse_mode='HTML'
            )
        except TelegraphException as er:
            if str(er) == "TITLE_TOO_LONG":
                return JSONResponse(status_code=400, content={"error": "Слишком длинный заголовок"})
            if str(er) == "ACCESS_TOKEN_INVALID":
                return JSONResponse(status_code=400, content={"error": "Неверный токен!"})
            return JSONResponse(status_code=400, content={"error": "Неизвестная ошибка, попробуйте еще раз."})

        return f"Пост {post.telegraph_url} отредактирован"

    @catch_logs
    async def delete_post(self, user_id: str, post_url: str):
        post = self._repository_posts.get(telegraph_url=post_url)
        if post.author_id != user_id:
            return JSONResponse(cstatus_code=403, content={"error": "Вы не являетесь автором поста"})
        return self._repository_posts.delete(db_obj=post, commit=True)

    @catch_logs
    async def get_post(self, post_id: str):
        return self._repository_posts.get(id=post_id)

    @catch_logs
    async def all_user_posts(
            self,
            user_id: str,):
        user_id = self._repository_telegram_user.get(telegram_id=user_id).id
        return self._repository_posts.list(author_id=user_id, status=Posts.PostStatus.published)

    @catch_logs
    async def my_posts(self, user_id: str):
        representation = {
            "published": self._repository_posts.list(author_id=user_id, status=Posts.PostStatus.published),
            "not_approved": self._repository_posts.list(author_id=user_id, status=Posts.PostStatus.not_approved),
            "draft": {
                "posts": self._repository_posts.list(author_id=user_id, status=Posts.PostStatus.draft),
                "draft_count": self._repository_posts.count_draft_posts(author_id=user_id)[0]
            }
        }
        return representation

    @catch_logs
    async def all_types_posts(self, user_id: str):
        followings = self._repository_telegram_user.get(id=user_id).followings
        followings_ids = [following.id for following in followings]
        representaion = {
            "popular": self._repository_posts.most_popular().all(),
            "recent": self._repository_posts.most_recent().all(),
            "my_feed": self._repository_posts.feed(followings_ids=followings_ids).all()
        }
        return representaion

    @catch_logs
    async def popular_posts(self,):
        return paginate(self._repository_posts.most_popular())

    @catch_logs
    async def recent_posts(self,):
        return paginate(self._repository_posts.most_recent())

    @catch_logs
    async def my_feed(self, user_id: str):
        followings = self._repository_telegram_user.get(id=user_id).followings
        followings_ids = [following.id for following in followings]
        return paginate(self._repository_posts.feed(followings_ids=followings_ids))

    @catch_logs
    async def three_last_posts(self,):
        return self._repository_posts.three_last_posts()

    @catch_logs
    async def upload_image(
            self,
            user_id: str,
            image):
        user = self._repository_telegram_user.get(id=user_id)

        current_file = Path(__file__)
        current_file_dir = current_file.parent
        project_root = current_file_dir.parent.parent / f"image/{user.telegram_id}"
        project_root_absolute = project_root.resolve()
        random_name = randint(1, 100_000)
        static_root_absolute = project_root_absolute / f"{random_name}.png"
        file_location = static_root_absolute
        with open(file_location, "wb+") as file_object:
            image.filename = f"{random_name}.png"
            file_object.write(image.file.read())
        return JSONResponse(
            status_code=200,
            content={"img_path": f"/image/{user.telegram_id}/{image.filename}"}
        )

    @catch_logs
    async def upload_video(
            self,
            user_id: str,
            video):
        user = self._repository_telegram_user.get(id=user_id)

        current_file = Path(__file__)
        current_file_dir = current_file.parent
        project_root = current_file_dir.parent.parent / f"video/{user.telegram_id}"
        project_root_absolute = project_root.resolve()
        random_name = randint(1, 100_000)
        static_root_absolute = project_root_absolute / f"{random_name}.mp4"
        file_location = static_root_absolute
        with open(file_location, "wb+") as file_object:
            video.filename = f"{random_name}.mp4"
            file_object.write(video.file.read())
        return JSONResponse(
            status_code=200,
            content={"video_path": f"/video/{user.telegram_id}/{video.filename}"}
        )

    @catch_logs
    async def get_draft_post(self, user_id: str, post_id: str):
        post = self._repository_posts.get(id=post_id)
        if post.author_id != user_id:
            return JSONResponse(status_code=403, content="Это не ваша черновая статья.")
        return post

    @catch_logs
    async def list_draft_posts(self, user_id: str):
        user = self._repository_telegram_user.get(id=user_id)
        posts = self._repository_posts.list(
            author_id=user.id,
            status=Posts.PostStatus.draft
        )
        logger.info(posts)
        return posts

    @catch_logs
    async def leader_board(self):
        leader_board_stats = self._repository_posts.users_leader_board()
        stat_list = []
        for stats in leader_board_stats:
            user_stat = {
                "id": stats[0],
                "telegram_id": stats[1],
                "first_name": stats[2],
                "surname": stats[3],
                "username": stats[4],
                "views": stats[5],
                "reactions": stats[6],
                "comments": stats[7]
            }
            stat_list.append(user_stat)
        return stat_list