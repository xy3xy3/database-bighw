from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from admin.utils.commonModel import ResponseModel
from admin.utils.decorators import login_required
from models.HistoryModel import HistoryModel
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
router = APIRouter()

# 历史记录列表页面
@router.get("/history")
@login_required
async def history_list(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})

# 历史记录表单页面
@router.get("/history_form")
@login_required
async def history_form(request: Request):
    return templates.TemplateResponse("history_form.html", {"request": request})

# 搜索历史记录
@router.post("/history/search")
@login_required
async def history_search(request: Request, page: int = 1, limit: int = 10, agent_id: int = None):
    history_model = HistoryModel()
    conditions = {}
    if agent_id:
        conditions["agent_id"] = agent_id
    paginated_data = history_model.get_paginated(page=page, per_page=limit, conditions=conditions)
    return ResponseModel(
        code=0,
        msg="Success",
        data=paginated_data["data"],
        count=paginated_data["total"]
    )

# 保存历史记录
@router.post("/history/save")
@login_required
async def history_save(request: Request):
    form_data = await request.form()
    history_model = HistoryModel()

    history_id = form_data.get("id")
    if history_id:
        history_id = int(history_id)
    flag = form_data.get("flag")
    agent_id = form_data.get("agent_id")

    if history_id:
        history_model.update(history_id, {
            "flag": flag,
            "agent_id": agent_id
        })
        msg = "历史记录更新成功"
    else:
        history_model.create_history(flag, agent_id)
        msg = "历史记录创建成功"

    return ResponseModel(
        code=0,
        msg=msg
    )

# 删除历史记录
@router.post("/history/del")
@login_required
async def history_del(request: Request):
    form_data = await request.form()
    history_id = form_data.get("id")
    history_model = HistoryModel()

    if history_id:
        history_model.delete(history_id)
        return ResponseModel(
            code=0,
            msg="历史记录删除成功"
        )
    return ResponseModel(
        code=1,
        msg="历史记录 ID 不能为空"
    )