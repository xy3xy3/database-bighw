# -*- coding: utf-8 -*-
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from admin.router import admin_router
from utils import *  # 用于密码哈希等
from database import init_db, reset_db  # 导入数据库初始化函数
from contextlib import asynccontextmanager

# 定义 lifespan 管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行的操作
    reset_db() # 清空数据库，测试阶段使用
    init_db()  # 初始化数据库
    yield  # 在这里切换到应用程序的运行阶段
    # 应用关闭时执行的操作（如果有）

# 使用 lifespan 管理生命周期
app = FastAPI(title="在线购物系统", lifespan=lifespan)

# 获取项目的根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 配置静态文件路径
ADMIN_STATIC_DIR = os.path.join(BASE_DIR, "app", "admin", "static")
app.mount("/admin/static", StaticFiles(directory=ADMIN_STATIC_DIR), name="admin_static")

app.include_router(admin_router)

@app.get("/")
async def root():
    return {"message": "欢迎使用在线购物系统"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=666, reload=True)
