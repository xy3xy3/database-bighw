from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from admin.utils.commonModel import ResponseModel
from admin.utils.decorators import login_required
from models.AgentModel import AgentModel
from models.ModelModel import ModelModel 

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
router = APIRouter()

# Agent列表页面
@router.get("/agent")
@login_required
async def agent_list(request: Request):
    model = ModelModel()
    mapping = model.get_map("id","name")
    return templates.TemplateResponse("agent.html",  {"request": request,"mapping":mapping})

# Agent表单页面
@router.get("/agent_form")
@login_required
async def agent_form(request: Request):
    model_model = ModelModel()
    models = model_model.get_options_list("id","name")  # 获取所有模型数据
    print(models)
    return templates.TemplateResponse("agent_form.html", {"request": request, "models": models})
# 搜索Agent
@router.post("/agent/search")
@login_required
async def agent_search(request: Request, page: int = 1, limit: int = 10, name: Optional[str] = None):
    agent_model = AgentModel()
    conditions = {}
    paginated_data = agent_model.get_paginated(page=page, per_page=limit, conditions=conditions)

    return ResponseModel(
        code=0,
        msg="Success",
        data=paginated_data["data"],
        count=paginated_data["total"]
    )

# 保存Agent
@router.post("/agent/save")
@login_required
async def agent_save(request: Request):
    form_data = await request.form()
    agent_model = AgentModel()

    agent_id = form_data.get("id")
    if agent_id:
        agent_id = int(agent_id)
    name = form_data.get("name")
    base_ids = form_data.get("base_ids")
    max_ref = int(form_data.get("max_ref"))
    min_cor = float(form_data.get("min_cor"))
    q_model_id = int(form_data.get("q_model_id"))
    q_prompt = form_data.get("q_prompt")
    a_model_id = int(form_data.get("a_model_id"))
    a_prompt = form_data.get("a_prompt")

    if agent_id:
        agent_model.update_agent(agent_id, name=name, base_ids=base_ids, max_ref=max_ref,
                                 min_cor=min_cor, q_model_id=q_model_id, q_prompt=q_prompt,
                                 a_model_id=a_model_id, a_prompt=a_prompt)
        msg = "Agent更新成功"
    else:
        agent_model.create_agent(name=name, base_ids=base_ids, max_ref=max_ref, min_cor=min_cor,
                                 q_model_id=q_model_id, q_prompt=q_prompt,
                                 a_model_id=a_model_id, a_prompt=a_prompt)
        msg = "Agent创建成功"

    return ResponseModel(
        code=0,
        msg=msg
    )

# 删除Agent
@router.post("/agent/del")
@login_required
async def agent_del(request: Request):
    form_data = await request.form()
    agent_id = form_data.get("id")
    agent_model = AgentModel()

    if agent_id:
        agent_model.delete_agent(agent_id)
        return ResponseModel(
            code=0,
            msg="Agent删除成功"
        )
    return ResponseModel(
        code=1,
        msg="Agent ID 不能为空"
    )
