from fastapi import APIRouter
from admin.controller.user import router as user_router

admin_router = APIRouter()
admin_router.include_router(user_router)