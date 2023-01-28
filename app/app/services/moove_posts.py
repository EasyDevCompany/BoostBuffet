import requests
from bs4 import BeautifulSoup

from fastapi.responses import JSONResponse
from fastapi_pagination.ext.sqlalchemy import paginate

from app.repository.moove_posts import RepositoryMoovePosts
from app.repository.telegram_user import RepositoryTelegramUser

from app.logs.logger_config import catch_logs


class MoovePostsService:

    def __init__(
            self,
            repository_telegram_user: RepositoryTelegramUser,
            moove_posts_repository: RepositoryMoovePosts) -> None:

        self._moove_posts_repository = moove_posts_repository
        self._repository_telegram_user = repository_telegram_user

    @catch_logs
    async def upload_post_url(self, url: str, category: str, user_id: str):
        user = self._repository_telegram_user.get(id=user_id)
        if user.role != "moderator":
            return JSONResponse(content={"error_msg": "У вас недостаточно прав"}, status_code=403)
        response = requests.get(url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "lxml")

        metas = [meta.attrs for meta in soup.find_all("meta")]
        for meta_tag in metas:
            if meta_tag.get("property") == "og:image":
                image_url = meta_tag.get("content").strip()
            elif meta_tag.get("property") == "og:description" or meta_tag.get("name") == "og:description":
                snippet = meta_tag.get("content").strip()
            elif meta_tag.get("property") == "og:title" or meta_tag.get("name") == "og:title":
                title = meta_tag.get("content").strip()

        return self._moove_posts_repository.create(
            obj_in={
                "title": title,
                "snippet": snippet,
                "post_url": url,
                "image_url": image_url,
                "category": category
            }, commit=True
        )

    @catch_logs
    async def all_posts(self, category: str):
        if not category:
            return paginate(self._moove_posts_repository.all_posts())
        return paginate(self._moove_posts_repository.filter_category(category=category))

    @catch_logs
    async def three_last_mooove_posts(self):
        return self._moove_posts_repository.three_last_mooove_posts()

    @catch_logs
    async def all_cateogories(self):
        categories = ["Питчинг", "Лекции", "Стартапы выпускников", "Читать буквы"]
        return JSONResponse(content={"categories": categories}, status_code=200)
