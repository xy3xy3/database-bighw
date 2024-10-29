from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from utils import res_suc, res_err
from database import db
from models.ConfigModel import ConfigModel
import os

# 获取项目的根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 构建模板目录的绝对路径
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
router = APIRouter()

@router.get("/admin/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/admin/doLogin")
async def doLogin(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    config = ConfigModel()
    admi_user = config.get_config("admi_user")
    admin_pwd = config.get_config("admin_pwd")
    print(admi_user,admin_pwd)
    # 验证账号密码
    if username == admi_user and password == admin_pwd:
        return res_suc("登录成功")
    else:
        return res_err("登录失败")