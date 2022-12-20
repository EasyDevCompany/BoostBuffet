from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from dependency_injector.wiring import inject, Provide
from app.core.containers import Container
from functools import wraps
from app.db.session import scope
from uuid import uuid4


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@inject
async def create_session():
    scope.set(str(uuid4()))


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
