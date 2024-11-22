from typing import Optional
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from admin.utils.commonModel import ResponseModel
from admin.utils.decorators import login_required
from models.ModelModel import ModelModel
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
router = APIRouter()

# 模型列表页面
@router.get("/model")
@login_required
async def model_list(request: Request):
    return templates.TemplateResponse("model.html", {"request": request})

# 模型表单页面
@router.get("/model_form")
@login_required
async def model_form(request: Request):
    return templates.TemplateResponse("model_form.html", {"request": request})

# 搜索模型
@router.post("/model/search")
@login_required
async def model_search(
    request: Request,
    page: int = Form(1),
    limit: int = Form(10),
    name: Optional[str] = Form(None)
):
    print(name)
    model_model = ModelModel()
    conditions = {}
    if name:
        conditions["name"] = name
    paginated_data = model_model.get_paginated(page=page, per_page=limit, conditions=conditions)
    return ResponseModel(
        code=0,
        msg="Success",
        data=paginated_data["data"],
        count=paginated_data["total"]
    )

# 保存模型
@router.post("/model/save")
@login_required
async def model_save(request: Request):
    form_data = await request.form()
    model_model = ModelModel()

    model_id = form_data.get("id")
    if model_id:
        model_id = int(model_id)
    name = form_data.get("name")
    base_url = form_data.get("base_url")
    api_key = form_data.get("api_key")
    model_type = int(form_data.get("type", 0))

    if model_id:
        model_model.update_model(model_id, name=name, base_url=base_url, api_key=api_key, model_type=model_type)
        msg = "模型更新成功"
    else:
        model_model.create_model(name, base_url, api_key, model_type)
        msg = "模型创建成功"

    return ResponseModel(
        code=0,
        msg=msg
    )

# 删除模型
@router.post("/model/del")
@login_required
async def model_del(request: Request):
    form_data = await request.form()
    model_id = form_data.get("id")
    model_model = ModelModel()

    if model_id:
        model_model.delete_model(int(model_id))
        return ResponseModel(
            code=0,
            msg="模型删除成功"
        )
    return ResponseModel(
        code=1,
        msg="模型 ID 不能为空"
    )