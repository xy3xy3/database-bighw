# -*- coding: utf-8 -*-
from fastapi import FastAPI
from admin.router import admin_router
from utils import *  # 用于密码哈希等
from database import init_db  # 导入数据库初始化函数
from contextlib import asynccontextmanager

# 定义 lifespan 管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行的操作
    init_db()  # 初始化数据库
    yield  # 在这里切换到应用程序的运行阶段
    # 应用关闭时执行的操作（如果有）

# 使用 lifespan 管理生命周期
app = FastAPI(title="在线购物系统", lifespan=lifespan)

app.include_router(admin_router)

@app.get("/")
async def root():
    return {"message": "欢迎使用在线购物系统"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=666)