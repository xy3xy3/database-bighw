from hashlib import md5
from fastapi import APIRouter, Request, Depends, Response
from fastapi.templating import Jinja2Templates
from admin.utils.commonModel import ResponseModel
from database import db
from models.ConfigModel import ConfigModel
from session import create_session  # 导入会话管理函数
import os
from loguru import logger  # 假设使用loguru记录日志
import traceback

router = APIRouter()

# 获取项目的根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 构建模板目录的绝对路径
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/doLogin")
async def doLogin(request: Request, response: Response):
    try:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        print(f" User: {username},  Password: {password}")
        config = ConfigModel()
        admin_user = await config.get_config("admin_user")
        admin_pwd = await config.get_config("admin_pwd")
        print(f"Admin User: {admin_user}, Admin Password: {admin_pwd}")
        # 验证账号密码
        if username == admin_user and password == admin_pwd:
            str = (username + password).encode()
            auth_key = md5(str).hexdigest()
            create_session(response, "admin_login", auth_key)  # 设置会话
            return ResponseModel(
                code=0,
                msg="登录成功",
                data={"redirect_url": "/admin/"}  # 返回重定向URL
            )
        else:
            return ResponseModel(
                code=1,
                msg="登录失败",
                data=None
            )
    except Exception as e:
        errmsg = f"登录失败{e} {traceback.format_exc()}"
        return ResponseModel(
            code=1,
            msg=errmsg,
            data=None
        )