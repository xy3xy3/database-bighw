from typing import Optional
from fastapi import APIRouter, Form, Request, Depends
from fastapi.templating import Jinja2Templates
from admin.utils.commonModel import ResponseModel
from admin.utils.decorators import login_required
from models.AgentModel import AgentModel
from models.MessageModel import MessageModel
from models.HistoryModel import HistoryModel  # 导入 HistoryModel
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
router = APIRouter()

# 消息列表页面


@router.get("/message")
@login_required
async def message_list(request: Request):
    agent_model = AgentModel()
    agent_mapping = await agent_model.get_map("id", "name")  # 获取 Agent 映射
    agents = await agent_model.get_options_list("id", "name")  # 获取选项列表
    return templates.TemplateResponse(
        "message.html", {
            "request": request, "agents": agents, "agent_mapping": agent_mapping
        }
    )
# 消息表单页面


@router.get("/message_form")
@login_required
async def message_form(request: Request):
    agent_model = AgentModel()
    agents = await agent_model.get_options_list("id", "name")  # 获取选项列表
    return templates.TemplateResponse(
        "message_form.html", {"request": request, "agents": agents}
    )

# 搜索消息


@router.post("/message/search")
@login_required
async def message_search(
    request: Request,
    page: int = Form(1),
    limit: int = Form(10),
    session_id: Optional[str] = Form(None),
    agent_id: Optional[str] = Form(None)  # 添加 agent_id 参数
):
    message_model = MessageModel()
    conditions = {}
    if session_id:
        conditions["session_id"] = session_id
    if agent_id:
        conditions["agent_id"] = int(agent_id)  # 添加 agent_id 过滤条件

    paginated_data = await message_model.get_paginated(page=page, per_page=limit, conditions=conditions)

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
    agent_id = form_data.get("agent_id")  # 获取 agent_id

    if message_id:
        data = {
            "role": role,
            "content": content,
            "agent_id": agent_id  # 更新 agent_id
        }
        await message_model.update(message_id, data)
        msg = "消息更新成功"
    else:
        data = {
            "history_id": history_id,
            "role": role,
            "content": content,
            "agent_id": agent_id  # 保存 agent_id
        }
        await message_model.save(data)
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
        await message_model.delete(message_id)
        return ResponseModel(
            code=0,
            msg="消息删除成功"
        )
    return ResponseModel(
        code=1,
        msg="消息 ID 不能为空"
    )

# 批量删除消息


@router.post("/message/del_batch")
@login_required
async def message_batch_del(request: Request):
    form_data = await request.form()
    ids = form_data.getlist("ids[]")
    model = MessageModel()
    if ids:
        ids = [int(id) for id in ids]
        await model.batch_delete(ids)
        return ResponseModel(
            code=0,
            msg="消息批量删除成功"
        )
    return ResponseModel(
        code=1,
        msg="消息 ID 不能为空"
    )
