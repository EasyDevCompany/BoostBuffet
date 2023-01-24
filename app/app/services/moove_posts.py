import requests
from bs4 import BeautifulSoup
from app.repository.moove_posts import RepositoryMoovePosts

from fastapi.responses import JSONResponse



class MoovePostsService:

    def __init__(
            self,
            moove_posts_repository: RepositoryMoovePosts) -> None:

        self._moove_posts_repository = moove_posts_repository

    async def upload_post_url(self, url: str, category: str):
        response = requests.get(url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "lxml")

        metas = [meta.attrs for meta in soup.find_all("meta")]
        for meta_tag in metas:
            if meta_tag.get("property") == "og:image":
                image_url = meta_tag.get("content").strip()
            elif meta_tag.get("property") == "og:description":
                snippet = meta_tag.get("content").strip()
            elif meta_tag.get("property") == "og:title":
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

    async def all_posts(self):
        return self._moove_posts_repository.list()

    async def all_cateogories(self):
        categories = ["Питчинг", "Лекции", "Стартапы выпускников", "Читать буквы"]
        return JSONResponse(content={"categories": categories}, status_code=200)
