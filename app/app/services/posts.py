from pathlib import Path
from random import randint

from fastapi.responses import JSONResponse

from telegraph import Telegraph
from telegraph.exceptions import TelegraphException

from app.core.config import settings

from app.models.telegram_user import TelegramUser
from app.models.posts import Posts

from app.repository.posts import RepositoryPosts, Posts
from app.repository.telegram_user import RepositoryTelegramUser

from app.telegram_bot.loader import bot

from app.schemas.posts import PostIn


class PostsService:

    def __init__(
            self,
            repository_telegram_user: RepositoryTelegramUser,
            repository_posts: RepositoryPosts,) -> None:

        self._repository_telegram_user = repository_telegram_user
        self._repository_posts = repository_posts

    async def create_post(self, user_id: str, post_in: PostIn):
        user = self._repository_telegram_user.get(id=user_id)
        telegraph = Telegraph(user.telegraph_access_token)
        try:
            post = telegraph.create_page(
                post_in.title or '',
                html_content=post_in.content
            )
            post = self._repository_posts.create(
                obj_in={
                    "telegraph_url": post.get("url"),
                    "path": post.get("path"),
                    "title": post.get("title"),
                    "content": post_in.content,
                    "status": Posts.PostStatus.published,
                    "author": user,
                }, commit=True)

            await bot.send_message(
                user.telegram_id,
                "Ваш пост опубликовали",
                parse_mode='HTML'
            )
            message = await bot.send_message(
                "-1001447940387",
                f'<a href="{post.telegraph_url}">{post.title}</a>',
                parse_mode='HTML'
            )
            await bot.forward_message(
                chat_id=user.telegram_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )

        except TelegraphException as er:
            if str(er) == "TITLE_TOO_LONG":
                return JSONResponse(status_code=400, content={"error": "Слишком длинный заголовок"})
            if str(er) == "ACCESS_TOKEN_INVALID":
                return JSONResponse(status_code=400, content={"error": "Неверный токен!"})
            return JSONResponse(status_code=400, content={"error": "Неизвестная ошибка, попробуйте еще раз."})

        return f"Пост {post.telegraph_url} отправлен на модерацию"

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
                    "status": Posts.PostStatus.published
                }
            )
            await bot.send_message(
                user.telegram_id,
                f'Вы отредактировали пост <a href="{post.telegraph_url}">{post.title}</a>',
                parse_mode='HTML'
            )
        except TelegraphException as er:
            if str(er) == "TITLE_TOO_LONG":
                return JSONResponse(status_code=400, content={"error": "Слишком длинный заголовок"})
            if str(er) == "ACCESS_TOKEN_INVALID":
                return JSONResponse(status_code=400, content={"error": "Неверный токен!"})
            return JSONResponse(status_code=400, content={"error": "Неизвестная ошибка, попробуйте еще раз."})

        return f"Пост {post.telegraph_url} отредактирован"

    async def delete_post(self, user_id: str, post_url: str):
        post = self._repository_posts.get(telegraph_url=post_url)
        if post.author_id != user_id:
            return JSONResponse(cstatus_code=403, content={"error": "Вы не являетесь автором поста"})
        return self._repository_posts.delete(db_obj=post, commit=True)

    async def all_user_posts(
            self,
            user_id: str,):
        user_id = self._repository_telegram_user.get(telegram_id=user_id).id
        return self._repository_posts.list(author_id=user_id, status=Posts.PostStatus.published)

    async def my_posts(self, user_id: str):
        representation = {
            "published": self._repository_posts.list(author_id=user_id, status=Posts.PostStatus.published),
            "draft": {
                "posts": self._repository_posts.list(author_id=user_id, status=Posts.PostStatus.draft),
                "draft_count": self._repository_posts.count_draft_posts(author_id=user_id)[0]
            }
        }
        return representation

    async def all_types_posts(self, user_id: str):
        followings = self._repository_telegram_user.get(id=user_id).followings
        followings_ids = [following.id for following in followings]
        representaion = {
            "popular": self._repository_posts.most_popular(),
            "recent": self._repository_posts.most_recent(),
            "my_feed": self._repository_posts.feed(followings_ids=followings_ids)
        }
        return representaion

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
            content={"img_url": f"{settings.SERVER_IP}/image/{user.telegram_id}/{image.filename}"}
        )

    async def update_status(self, post_id: str, user_id: str, status: str):
        user = self._repository_telegram_user.get(id=user_id)
        if user.role != TelegramUser.UserRole.moderator:
            return JSONResponse(status_code=403, content={"error": "У вас нет на это прав"})

        post = self._repository_posts.get(id=post_id)
        post = self._repository_posts.update(
                db_obj=post,
                obj_in={
                    "status": status
                }
            )

        if status == Posts.PostStatus.published:
            await bot.send_message(
                post.author.telegram_id,
                f'Ваш пост <a href="{post.telegraph_url}">{post.title}</a> был опубликован',
                parse_mode='HTML'
            )
            return JSONResponse(status_code=400, content={"error": "Новый статус: опубликован"})

        await bot.send_message(
            post.author.telegram_id,
            f'Ваш пост <a href="{post.telegraph_url}">{post.title}</a> не прошел модерацию.',
            parse_mode='HTML'
        )
        return JSONResponse(status_code=400, content={"error": "Новый статус: не прошёл модерацию."})
