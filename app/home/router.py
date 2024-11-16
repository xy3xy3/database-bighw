from fastapi import APIRouter

home_router = APIRouter()

from home.controller.index import router as index_router
home_router.include_router(index_router)
