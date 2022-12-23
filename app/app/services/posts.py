from fastapi.responses import JSONResponse

from telegraph import Telegraph
from telegraph.exceptions import TelegraphException

from typing import Optional

from app.repository.posts import RepositoryPosts, Posts
from app.repository.telegram_user import RepositoryTelegramUser

from app.exceptions.posts import post_exceptions


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
            self._repository_posts.create(
                obj_in={
                    "telegraph_url": post.get("url"),
                    "path": post.get("path"),
                    "title": post.get("title"),
                    "status": Posts.PostStatus.not_published,
                    "author": user,
                }, commit=True
            )
        except TelegraphException as er:
            if str(er) == "TITLE_TOO_LONG":
                return JSONResponse(status_code=400, content="Слишком длинный заголовок")
            if str(er) == "ACCESS_TOKEN_INVALID":
                return JSONResponse(status_code=400, content="Неверный токен!")
            return "Неизвестная ошибка, попробуйте еще раз."
        return "Пост отправлен на модерацию"

    async def edit_post(
            self,
            user_id: str,
            post_id: str,
            title: Optional[str],
            content: Optional[str]):

        user = self._repository_telegram_user.get(id=user_id)
        post = self._repository_posts.get(id=post_id)
        if post.author != user:
            return JSONResponse(status_code=403, content="Вы не являетесь автором поста")

        telegraph = Telegraph(user.telegraph_access_token)
        try:
            post = self._repository_posts.get(id=post_id)
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
                    "status": Posts.PostStatus.not_published
                }
            )
        except TelegraphException as er:
            if str(er) == "TITLE_TOO_LONG":
                return JSONResponse(status_code=400, content="Слишком длинный заголовок")
            if str(er) == "ACCESS_TOKEN_INVALID":
                return JSONResponse(status_code=400, content="Неверный токен!")
            return "Неизвестная ошибка, попробуйте еще раз."
        return "Пост отправлен на модерацию"

    async def update_status(self, post_id: str, user_id: str, status: str):
        user = self._repository_telegram_user.get(id=user_id)
        print(user.UserRole)
        if user.UserRole != "moderator":
            return JSONResponse(status_code=403, content="У вас нет на это прав")
        post = self._repository_posts.get(id=post_id)
        self._repository_posts.update(
                db_obj=post,
                obj_in={
                    "status": status
                }
            )
