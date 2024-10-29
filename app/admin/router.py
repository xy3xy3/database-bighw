from fastapi import APIRouter

admin_router = APIRouter()

from admin.controller.user import router as user_router
admin_router.include_router(user_router)

from admin.controller.login import router as login_router
admin_router.include_router(login_router)