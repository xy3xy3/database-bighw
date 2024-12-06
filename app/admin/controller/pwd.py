from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from admin.utils.commonModel import ResponseModel
from admin.utils.decorators import login_required
from models.ConfigModel import ConfigModel
from hashlib import md5
import os

router = APIRouter()

# 获取项目的根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 构建模板目录的绝对路径
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/pwd")
@login_required
async def pwd(request: Request):
    """显示修改密码的表单页面"""
    view = {"request": request,"title": "修改密码", "url": "pwd"}
    return templates.TemplateResponse("pwd.html", view)

@router.post("/pwd")
@login_required
async def pwd(
    request: Request,
    old_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...)
):
    """处理密码修改请求"""
    try:
        config_model = ConfigModel()
        admin_user = await config_model.get_config("admin_user")
        admin_pwd = await config_model.get_config("admin_pwd")

        # 验证旧密码是否正确
        if old_password != admin_pwd:
            return ResponseModel(code=1, msg="旧密码不正确", data=None)

        # 验证新密码和确认密码是否一致
        if new_password != confirm_password:
            return ResponseModel(code=1, msg="新密码和确认密码不一致", data=None)

        await config_model.update_config("admin_pwd", new_password)

        return ResponseModel(code=0, msg="密码修改成功", data=None)

    except Exception as e:
        return ResponseModel(code=1, msg=f"密码修改失败: {str(e)}", data=None)