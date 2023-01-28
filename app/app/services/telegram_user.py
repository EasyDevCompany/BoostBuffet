from pathlib import Path

from fastapi.responses import FileResponse

from app.repository.telegram_user import RepositoryTelegramUser

from app.logs.logger_config import catch_logs

class TelegramUserService:

    def __init__(
            self,
            repository_telegram_user: RepositoryTelegramUser,) -> None:

        self._repository_telegram_user = repository_telegram_user

    @catch_logs
    async def my_profile(self, user_id):
        user = self._repository_telegram_user.get(id=user_id)
        return user
