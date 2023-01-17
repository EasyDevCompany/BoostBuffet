import requests

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
            *args, **kwargs
    ):
        self._repository_posts = repository_posts
        self._phone = phone
        self._api_id = api_id,
        self._api_hash = api_hash
        self._channel_url = channel_url
        super().__init__(*args, **kwargs)

    async def client(self):
        client = TelegramClient(
            session=self.session_name,
            api_id=self._api_id[0],
            api_hash=self._api_hash
        )
        return await client.start(phone=self._phone)

    async def proccess(self, *args, **kwargs):
        client = await self.client()
        entity = await client.get_entity(self._channel_url)
        async for message in client.iter_messages(entity):
            if message.message is not None:
                reaction_count = 0
                comments_count = 0
                post_url = message.message.split("\n")[-1]

                if message.reactions is not None:
                    for reaction in message.reactions.results:
                        reaction_count += reaction.count

                if message.replies is not None:
                    comments_count = message.replies.replies

                post = self._repository_posts.get(telegraph_url=post_url[-1])
                
                if post is not None:
                    views = await self._get_post_views(post=post)
                    logger.info(f"Message: {post_url}\nReaction count: {reaction_count}\nComments count: {comments_count}")
                    self._repository_posts.update(
                        obj_in={
                            "likes_amount": reaction_count,
                            "comments_count": comments_count,
                            "views_count": views
                        },
                        db_obj=post
                    )
        await client.disconnect()

    async def _get_post_views(self, post):
        url = f"https://api.telegra.ph/getViews/{post.path}?year=2022"
        return requests.get(url).json().get("result").get("views")


    @property
    def session_name(self):
        return f"boost_{self._api_id[0]}"
