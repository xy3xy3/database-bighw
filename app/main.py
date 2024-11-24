# -*- coding: utf-8 -*-
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from admin.router import admin_router
from test.router import test_router
from api.router import api_router
from middleware.auth import AdminAuthMiddleware
from utils import *  # 用于密码哈希等
from database import init_db, reset_db  # 导入数据库初始化函数
from contextlib import asynccontextmanager

# 定义 lifespan 管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行的操作
    test = 0
    if test:
        reset_db()
        init_db()
    yield  # 在这里切换到应用程序的运行阶段
    # 应用关闭时执行的操作（如果有）

# 使用 lifespan 管理生命周期
app = FastAPI(title="在线购物系统", lifespan=lifespan)

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
app.mount("/api", api_app)

# home_app = FastAPI()
# home_app.include_router(home_router)

# # 挂载首页静态资源
# HOME_STATIC_DIR = os.path.join(BASE_DIR, "app", "home", "static")
# app.mount("/static", StaticFiles(directory=HOME_STATIC_DIR), name="home_static")

# app.mount("/", home_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=666, reload=True)
