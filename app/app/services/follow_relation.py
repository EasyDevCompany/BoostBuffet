from fastapi.responses import JSONResponse

from app.repository.telegram_user import RepositoryTelegramUser, FollowRelationship


class FollowService:

    def __init__(
            self,
            repository_telegram_user: RepositoryTelegramUser,
            repository_follow_relation: FollowRelationship) -> None:

        self._repository_telegram_user = repository_telegram_user
        self._repository_follow_relation = repository_follow_relation

    async def create_follow(
            self,
            follower_id: str,
            following_id: str):

        if follower_id == following_id:
            return JSONResponse("Вы не можете подписаться на самого себя", status_code=400)
        if self._repository_follow_relation.get(FollowerID=follower_id, FollowingID=following_id):
            return JSONResponse("Вы уже подписаны на этого пользователя", status_code=400)

        return self._repository_follow_relation.create(
            obj_in={
                "FollowerID": follower_id,
                "FollowingID": following_id
            }, commit=True)

