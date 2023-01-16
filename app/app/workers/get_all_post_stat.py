from .base import Base
from telethon import TelegramClient
from loguru import logger
from app.core.config import settings
from app.repository.posts import RepositoryPosts


class AllPostTask(Base):

    def __init__(
            self,
            phone: str,
            api_id: int,
            api_hash: str,
            channel_url: str,
            bot_token: str,
            repository_posts: RepositoryPosts,
            *args, **kwargs
    ):
        self._repository_posts = repository_posts
        self._phone = phone
        self._api_id = api_id,
        self._api_hash = api_hash
        self._channel_url = channel_url
        self._bot_token = bot_token
        super().__init__(*args, **kwargs)

    def client(self):
        return TelegramClient(
            session=self.session_name,
            api_id=self._api_id[0],
            api_hash=self._api_hash
        ).start(phone=self._phone, bot_token=self._bot_token)

    async def proccess(self, *args, **kwargs):
        client = await self.client()
        entity = await client.get_entity(self._channel_url)
        posts = client.iter_messages(entity=entity)
        # entity = await self.started_client().get_entity(self._channel_url)
        # posts = self.started_client().iter_messages(entity=entity)
        for post in posts:
            logger.info(post.id)
            if post.reactions is not None:
                for reaction in post.reactions.results:
                    logger.info(reaction.count)
            if post.replies is not None:
                logger.info(post.replies)

    @property
    def session_name(self):
        return f"boost_{self._api_id[0]}"
