from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from admin.utils.commonModel import ResponseModel
from admin.utils.decorators import login_required
from database import db
from models.UserModel import UserModel
import os

# 获取项目的根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 构建模板目录的绝对路径
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
router = APIRouter()

#html部分
@login_required
@router.get("/admin/user")
async def user_list(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})

@login_required
@router.get("/admin/user_form")
async def user_form(request: Request):
    user_model = UserModel()
    users = user_model.query()
    return templates.TemplateResponse("user_form.html", {"request": request, "users": users})

#数据处理部分
@login_required
@router.post("/admin/user/search")
async def user_list_ajax(request: Request, page: int = 1, limit: int = 10,
                          name: Optional[str] = None, email: Optional[str] = None):
    user_model = UserModel()

    # 构建查询条件
    conditions = {}
    if name:
        conditions["name"] = name
    if email:
        conditions["email"] = email

    # 获取分页数据
    paginated_data = user_model.get_paginated(page=page, per_page=limit, conditions=conditions)
    # 构建ResponseModel并返回
    response = ResponseModel(
        code=0,
        msg="Success",
        data=paginated_data["data"],  # 返回当前页数据
        count=paginated_data["total"]  # 总记录数
    )

    return response

# 表单保存用户
@router.post("/admin/user/save")
@login_required
async def user_save(request: Request):
    form_data = await request.form()
    user_model = UserModel()

    user_id = form_data.get("id")  # 获取用户 ID，如果没有则为 None
    # 转为int
    if user_id is not None:
        user_id = int(user_id)
    name = form_data.get("name")
    email = form_data.get("email")
    pwd = form_data.get("pwd")
    balance = form_data.get("balance")
    if user_id is not None and user_id !=0:
        # 更新用户
        user = user_model.update(user_id, {
            "name": name,
            "email": email,
            "pwd": pwd,
            "balance": balance
        })
        msg = "用户更新成功"
    else:
        # 插入新用户
        user = user_model.create_user(name, email, pwd,balance)
        msg = "用户创建成功"

    # 返回操作结果
    return ResponseModel(
        code=0,
        msg=msg
    )


# 删除单个用户
@router.post("/admin/user/del")
@login_required
async def user_del(request: Request):
    form_data = await request.form()
    user_id = form_data.get("id")
    user_model = UserModel()

    if user_id:
        user_model.delete(user_id)
        return ResponseModel(
            code=0,
            msg="用户删除成功",
            data=None
        )
    return ResponseModel(
        code=1,
        msg="用户 ID 不能为空",
        data=None
    )


# 删除多个用户
@router.post("/admin/user/del_batch")
async def user_del_batch(request: Request):
    form_data = await request.form()
    user_ids = form_data.getlist("ids[]")  # 获取多个用户 ID

    if user_ids:
        user_model = UserModel()
        for user_id in user_ids:
            user_model.delete(user_id)  # 删除每个用户
        return ResponseModel(
            code=0,
            msg="批量删除成功",
            data=None
        )
    return ResponseModel(
        code=1,
        msg="用户 IDs 不能为空",
        data=None
    )
