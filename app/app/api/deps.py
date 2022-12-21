from fastapi import Depends, Header, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dependency_injector.wiring import inject, Provide
from app.core.containers import Container
from functools import wraps
from app.db.session import scope
from uuid import uuid4


@inject
async def create_session():
    scope.set(str(uuid4()))


@inject
async def bot_token_verification(
        token: str = Header(default=None, alias="TOKEN"),
        repository_telegram_user = Depends(Provide[Container.repository_telegram_user])
):
    if not token:
        raise HTTPException(403)
    user = repository_telegram_user.get(id=token)
    if not user or not token:
        raise HTTPException(403)
    return token


@inject
def commit_and_close_session(func):

    @wraps(func)
    @inject
    async def wrapper(db=Depends(Provide[Container.db]), *args, **kwargs,):
        scope.set(str(uuid4()))
        try:
            result = await func(*args, **kwargs)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e
        finally:
            # db.session.expunge_all()
            db.scoped_session.remove()

    return wrapper
