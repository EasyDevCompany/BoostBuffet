from .base import Base
from telethon import TelegramClient
from loguru import logger

from app.repository.posts import RepositoryPosts


class AllPostTask(Base):

    def __init__(
            self,
            phone: str,
            api_id: int,
            api_hash: str,
            channel_url: str,
            repository_posts: RepositoryPosts,
    ):
        self._repository_posts = repository_posts
        self._phone = phone
        self._api_id = api_id,
        self._api_hash = api_hash
        self._channel_url = channel_url
        super().__init__(*args, **kwargs)

    def client(self):
        return TelegramClient(
            session=self.session_name,
            api_id=self._api_id,
            api_hash=self._api_hash
        )

    async def proccess(self, *args, **kwargs):
        entity = await self.client().get_entity(self._channel_url)
        posts = self.client().iter_messages(entity=entity)
        for post in posts:
            logger.info(post.id)
            if post.reactions is not None:
                for reaction in post.reactions.results:
                    logger.info(reaction.count)
            if post.replies is not None:
                print(post.replies)

    @property
    def session_name(self):
        return f"{self._phone}_{self._api_id}"
