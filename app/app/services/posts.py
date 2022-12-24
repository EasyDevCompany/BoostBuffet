from fastapi.responses import JSONResponse

from telegraph import Telegraph
from telegraph.exceptions import TelegraphException

# from aiogram.me

from typing import Optional

from app.models.telegram_user import TelegramUser
from app.models.posts import Posts

from app.repository.posts import RepositoryPosts, Posts
from app.repository.telegram_user import RepositoryTelegramUser

from app.telegram_bot.loader import bot


class PostsService:
    def __init__(
            self,
            repository_telegram_user: RepositoryTelegramUser,
            repository_posts: RepositoryPosts,) -> None:

        self._repository_telegram_user = repository_telegram_user
        self._repository_posts = repository_posts

    async def create_post(self, user_id: str, title: Optional[str], content: str):
        user = self._repository_telegram_user.get(id=user_id)
        telegraph = Telegraph(user.telegraph_access_token)
        try:
            post = telegraph.create_page(
                title or '',
                html_content=content
            )
            post = self._repository_posts.create(
                obj_in={
                    "telegraph_url": post.get("url"),
                    "path": post.get("path"),
                    "title": post.get("title"),
                    "content": content,
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
                return JSONResponse(status_code=400, content="Слишком длинный заголовок")
            if str(er) == "ACCESS_TOKEN_INVALID":
                return JSONResponse(status_code=400, content="Неверный токен!")
            return "Неизвестная ошибка, попробуйте еще раз."

        return f"Пост {post.telegraph_url} отправлен на модерацию"

    async def edit_post(
            self,
            user_id: str,
            post_url: str,
            title: Optional[str],
            content: Optional[str]):

        user = self._repository_telegram_user.get(id=user_id)
        post = self._repository_posts.get(telegraph_url=post_url)
        if post.author != user:
            return JSONResponse(status_code=403, content="Вы не являетесь автором поста")

        telegraph = Telegraph(user.telegraph_access_token)
        try:
            telegraph.edit_page(
                path=post.path,
                title=title or post.title,
                html_content=content or post.content
            )
            self._repository_posts.update(
                db_obj=post,
                obj_in={
                    "title": title or post.title,
                    "content": content or post.content,
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
                return JSONResponse(status_code=400, content="Слишком длинный заголовок")
            if str(er) == "ACCESS_TOKEN_INVALID":
                return JSONResponse(status_code=400, content="Неверный токен!")
            return "Неизвестная ошибка, попробуйте еще раз."

        return f"Пост {post.telegraph_url} отредактирован"

    async def all_posts(
            self,
            user_id: str,):
        return self._repository_posts.list(author_id=user_id)

    async def update_status(self, post_id: str, user_id: str, status: str):
        user = self._repository_telegram_user.get(id=user_id)
        if user.role != TelegramUser.UserRole.moderator:
            return JSONResponse(status_code=403, content="У вас нет на это прав")

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
            return f"Новый статус: опубликован"

        await bot.send_message(
            post.author.telegram_id,
            f'Ваш пост <a href="{post.telegraph_url}">{post.title}</a> не прошел модерацию.',
            parse_mode='HTML'
        )
        return f"Новый статус: не прошёл модерацию"
