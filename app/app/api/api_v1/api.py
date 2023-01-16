from fastapi import APIRouter, Depends
from app.api.deps import create_session
from app.api.api_v1.endpoints import webhook, posts, telegram_user, cards


api_router = APIRouter()

api_router.include_router(webhook.router, prefix="/webhook", tags=['webhook'])
api_router.include_router(posts.router, prefix="/posts", tags=['posts'])
api_router.include_router(telegram_user.router, prefix="/telegram_user", tags=['telegram_user'])
api_router.include_router(cards.router, prefix="/cards", tags=['cards'])