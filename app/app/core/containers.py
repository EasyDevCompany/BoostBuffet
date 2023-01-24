"""Containers module."""
from telegraph import Telegraph

from dependency_injector import containers, providers

from app.core.config import Settings
from app.core.celery import celery_app
from app.db.session import SyncSession

from app.repository.telegram_user import TelegramUser, FollowRelationship, RepositoryTelegramUser, RepositoryFollowRelationship
from app.repository.posts import Posts, RepositoryPosts
from app.repository.cards import RepositoryCards, Cards
from app.repository.moove_posts import RepositoryMoovePosts, MoovePosts

from app.services.posts import PostsService
from app.services.follow_relation import FollowService
from app.services.telegram_user import TelegramUserService
from app.services.cards import CardsService
from app.services.moove_posts import MoovePostsService

from app.workers.get_all_post_stat import AllPostTask

from app import redis


class CustomTaskProvider(providers.Provider):

    __slots__ = ("_singleton",)

    def __init__(self, provides, *args, **kwargs):
        self._singleton = providers.Singleton(provides, *args, **kwargs)
        custom_task = self._singleton.provided()
        celery_app.register_task(custom_task)
        super().__init__()

    def __deepcopy__(self, memo):
        copied = memo.get(id(self))
        if copied is not None:
            return copied

        copied = self.__class__(
            self._singleton.provides,
            *providers.deepcopy(self._singleton.args, memo),
            **providers.deepcopy(self._singleton.kwargs, memo),
        )
        self._copy_overridings(copied, memo)

        return copied

    @property
    def related(self):
        """Return related providers generator."""
        yield from [self._singleton]
        yield from super().related

    def _provide(self, *args, **kwargs):
        return self._singleton(*args, **kwargs)


class Container(containers.DeclarativeContainer):

    config = providers.Singleton(Settings)
    # Database block
    db = providers.Singleton(SyncSession, db_url=config.provided.SYNC_SQLALCHEMY_DATABASE_URI)
    telegraph = Telegraph()

    repository_telegram_user = providers.Singleton(RepositoryTelegramUser, model=TelegramUser, session=db)
    repository_follow_relation = providers.Singleton(RepositoryFollowRelationship, model=FollowRelationship, session=db)
    repository_posts = providers.Singleton(RepositoryPosts, model=Posts, session=db)
    reposotory_cards = providers.Singleton(RepositoryCards, model=Cards, session=db)
    reposotory_moove_posts = providers.Singleton(RepositoryMoovePosts, model=MoovePosts, session=db)

    telegram_user_service = providers.Singleton(
        TelegramUserService,
        repository_telegram_user=repository_telegram_user,
    )
    posts_service = providers.Singleton(
        PostsService,
        repository_telegram_user=repository_telegram_user,
        repository_posts=repository_posts,
    )
    follow_service = providers.Singleton(
        FollowService,
        repository_telegram_user=repository_telegram_user,
        repository_follow_relation=repository_follow_relation,
    )
    cards_service = providers.Singleton(
        CardsService,
        repository_cards=reposotory_cards,
        repository_telegram_user=repository_telegram_user
    )
    moove_posts_service = providers.Singleton(
        MoovePostsService,
        moove_posts_repository=reposotory_moove_posts
    )

    redis_pool = providers.Resource(
        redis.init_redis_pool,
        host=config.provided.REDIS_HOST
    )

    get_all_post_stat_task = CustomTaskProvider(
        AllPostTask,
        session=db,
        phone=config.provided.PHONE,
        api_id=config.provided.API_ID,
        api_hash=config.provided.API_HASH,
        channel_url=config.provided.CHANNEL_URL,
        repository_posts=repository_posts
    )


@containers.copy(Container)
class CeleryContainer(Container):
    config = providers.Singleton(Settings)
    db = providers.Singleton(SyncSession, db_url=config.provided.SYNC_SQLALCHEMY_DATABASE_URI, dispose_session=True)
