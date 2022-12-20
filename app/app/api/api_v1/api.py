from fastapi import APIRouter, Depends
from app.api.deps import create_session
from app.api.api_v1.endpoints import webhook


api_router = APIRouter()

api_router.include_router(webhook.router, prefix="/webhook", tags=['webhook'])
