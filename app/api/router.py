from fastapi import APIRouter
from api.controller import chat

api_router = APIRouter()
api_router.include_router(chat.router)
