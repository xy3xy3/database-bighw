from fastapi import APIRouter

admin_router = APIRouter()

from admin.controller.index import router as index_router
admin_router.include_router(index_router)



from admin.controller.login import router as login_router
admin_router.include_router(login_router)



from admin.controller.model import router as model_router
admin_router.include_router(model_router)

from admin.controller.knowledgebase import router as knowledgebase_router
admin_router.include_router(knowledgebase_router)


from admin.controller.history import router as history_router
admin_router.include_router(history_router)