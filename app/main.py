# -*- coding: utf-8 -*-
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from admin.router import admin_router
from test.router import test_router
from api.router import api_router
from home.router import home_router
from middleware.auth import AdminAuthMiddleware
from fastapi.middleware.cors import CORSMiddleware

from utils import *  # 用于密码哈希等
from database import init_db, reset_db  # 导入数据库初始化函数
from contextlib import asynccontextmanager
import logging

logging.basicConfig(level=logging.DEBUG)
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from database import db
# 定义 lifespan 管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_pool()
    # 启动时执行的操作
    test = 0
    if test:
        reset_db()
        init_db()
    yield  # 在这里切换到应用程序的运行阶段
    # 应用关闭时执行的操作（如果有）

# 使用 lifespan 管理生命周期
app = FastAPI(title="AI AGENT", lifespan=lifespan, debug=True)
# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，你可以根据需要限制特定的域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有头部
)
# bug显示

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logging.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse({
        "error": {
            "status_code": exc.status_code,
            "detail": exc.detail,
            "headers": exc.headers
        }
    })

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.error(f"General Exception: {exc}", exc_info=True)
    return JSONResponse({
        "error": {
            "status_code": 500,
            "detail": "Internal Server Error"
        }
    }, status_code=500)
# 获取项目的根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
admin_app = FastAPI()
admin_app.add_middleware(AdminAuthMiddleware)
admin_app.include_router(admin_router)

# 挂载admin静态资源
ADMIN_STATIC_DIR = os.path.join(BASE_DIR, "app", "admin", "static")
app.mount("/admin/static", StaticFiles(directory=ADMIN_STATIC_DIR), name="admin_static")

app.mount("/admin", admin_app)

test_app = FastAPI()
test_app.include_router(test_router)
app.mount("/test", test_app)


api_app = FastAPI()
api_app.include_router(api_router)
app.mount("/v1", api_app)

home_app = FastAPI()
home_app.include_router(home_router)

# 挂载首页静态资源
HOME_STATIC_DIR = os.path.join(BASE_DIR, "app", "home", "static")
app.mount("/static", StaticFiles(directory=HOME_STATIC_DIR), name="home_static")

app.mount("/", home_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=666, reload=True, debug=True)
