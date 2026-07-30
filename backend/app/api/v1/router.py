from fastapi import APIRouter
from app.api.v1 import chat, conversations, schemes, webhook

api_router = APIRouter()
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
api_router.include_router(schemes.router, prefix="/schemes", tags=["schemes"])
api_router.include_router(webhook.router, prefix="/webhook", tags=["webhook"])
