from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from admin.utils.commonModel import ResponseModel
from admin.utils.decorators import login_required
from models.MessageModel import MessageModel
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
router = APIRouter()

# 消息列表页面
@router.get("/message")
@login_required
async def message_list(request: Request):
    return templates.TemplateResponse("message.html", {"request": request})

# 消息表单页面
@router.get("/message_form")
@login_required
async def message_form(request: Request):
    return templates.TemplateResponse("message_form.html", {"request": request})

# 搜索消息
@router.post("/message/search")
@login_required
async def message_search(request: Request, page: int = 1, limit: int = 10, history_id: Optional[int] = None):
    message_model = MessageModel()
    conditions = {}
    if history_id:
        conditions["history_id"] = history_id
    paginated_data = message_model.get_paginated(page=page, per_page=limit, conditions=conditions)

    return ResponseModel(
        code=0,
        msg="Success",
        data=paginated_data["data"],
        count=paginated_data["total"]
    )

# 保存消息
@router.post("/message/save")
@login_required
async def message_save(request: Request):
    form_data = await request.form()
    message_model = MessageModel()

    message_id = form_data.get("id")
    if message_id:
        message_id = int(message_id)
    history_id = form_data.get("history_id")
    role = form_data.get("role")
    content = form_data.get("content")

    if message_id:
        message_model.update_message(message_id, role=role, content=content)
        msg = "消息更新成功"
    else:
        message_model.create_message(history_id, role, content)
        msg = "消息创建成功"

    return ResponseModel(
        code=0,
        msg=msg
    )

# 删除消息
@router.post("/message/del")
@login_required
async def message_del(request: Request):
    form_data = await request.form()
    message_id = form_data.get("id")
    message_model = MessageModel()

    if message_id:
        message_model.delete_message(message_id)
        return ResponseModel(
            code=0,
            msg="消息删除成功"
        )
    return ResponseModel(
        code=1,
        msg="消息 ID 不能为空"
    )
