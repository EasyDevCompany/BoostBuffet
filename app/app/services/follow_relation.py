from fastapi.responses import JSONResponse

from app.repository.telegram_user import RepositoryTelegramUser, FollowRelationship

from app.schemas.follow_relation import FollowIn

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
            follow_in: FollowIn):

        following_id = self._repository_telegram_user.get(telegram_id=follow_in.following_telegram_id).id
        if follower_id == following_id:
            return JSONResponse("Вы не можете подписаться на самого себя", status_code=400)
        if self._repository_follow_relation.get(FollowerID=follower_id, FollowingID=following_id):
            return JSONResponse("Вы уже подписаны на этого пользователя", status_code=400)
        return self._repository_follow_relation.create(
            obj_in={
                "FollowerID": follower_id,
                "FollowingID": following_id
            }, commit=True)

