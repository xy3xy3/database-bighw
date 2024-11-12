from fastapi import APIRouter

admin_router = APIRouter()

from admin.controller.index import router as index_router
admin_router.include_router(index_router)

from admin.controller.user import router as user_router
admin_router.include_router(user_router)

from admin.controller.category import router as category_router
admin_router.include_router(category_router)


from admin.controller.login import router as login_router
admin_router.include_router(login_router)


from admin.controller.order import router as order_router
admin_router.include_router(order_router)