# 修复后的 app\admin\controller\knowledgebase.py
import traceback
from typing import Optional
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from admin.utils.commonModel import ResponseModel
from admin.utils.decorators import login_required
from models.ModelModel import ModelModel
from models.KnowledgeBaseModel import KnowledgeBaseModel
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
router = APIRouter()

# 知识库列表页面
@router.get("/knowledgebase")
@login_required
async def knowledgebase_list(request: Request):
    try:
        model = ModelModel()
        mapping = await model.get_map("id","name")
        return templates.TemplateResponse("knowledgebase.html", {"request": request,"mapping":mapping})
    except Exception as e:
        errmsg = f"{e} {traceback.format_exc()}"
        return ResponseModel(
            code=1,
            msg=errmsg,
            data=None
        )

# 知识库表单页面
@router.get("/knowledgebase_form")
@login_required
async def knowledgebase_form(request: Request):
    model_model = ModelModel()  # 实例化模型数据访问对象
    conditions = {
        "model_type":0,
    }
    models = await model_model.get_options_list("id", "name",conditions)  # 获取模型列表
    return templates.TemplateResponse("knowledgebase_form.html", {"request": request, "models": models})


# 搜索知识库
@router.post("/knowledgebase/search")
@login_required
async def knowledgebase_search(
    request: Request,
    page: int = Form(1),
    limit: int = Form(10),
    name: Optional[str] = Form(None)
):
    knowledgebase_model = KnowledgeBaseModel()
    conditions = {}
    if name:
        conditions["name"] = name
    paginated_data = await knowledgebase_model.get_paginated(page=page, per_page=limit, conditions=conditions)
    return ResponseModel(
        code=0,
        msg="Success",
        data=paginated_data["data"],
        count=paginated_data["total"]
    )

# 保存知识库
@router.post("/knowledgebase/save")
@login_required
async def knowledgebase_save(request: Request):
    form_data = await request.form()
    knowledgebase_model = KnowledgeBaseModel()

    knowledgebase_id = form_data.get("id")
    if knowledgebase_id:
        knowledgebase_id = int(knowledgebase_id)
    name = form_data.get("name")
    description = form_data.get("description")
    model_id = int(form_data.get("model_id", 0))

    if knowledgebase_id:
        data = {
            "name": name,
            "description": description,
            "model_id": model_id
        }
        await knowledgebase_model.update(knowledgebase_id,data)
        msg = "知识库更新成功"
    else:
        data = {
            "name": name,
            "description": description,
            "model_id": model_id
        }
        await knowledgebase_model.save(data)
        msg = "知识库创建成功"

    return ResponseModel(
        code=0,
        msg=msg
    )

# 删除知识库
@router.post("/knowledgebase/del")
@login_required
async def knowledgebase_del(request: Request):
    form_data = await request.form()
    knowledgebase_id = form_data.get("id")
    knowledgebase_model = KnowledgeBaseModel()

    if knowledgebase_id:
        await knowledgebase_model.delete(int(knowledgebase_id))
        return ResponseModel(
            code=0,
            msg="知识库删除成功"
        )
    return ResponseModel(
        code=1,
        msg="知识库 ID 不能为空"
    )

# 批量删除
@router.post("/knowledgebase/del_batch")
@login_required
async def batch_del(request: Request):
    form_data = await request.form()
    ids = form_data.getlist("ids[]")
    model = KnowledgeBaseModel()
    if ids:
        ids = [int(id) for id in ids]
        await model.batch_delete(ids)
        return ResponseModel(
            code=0,
            msg="批量删除成功"
        )
    return ResponseModel(
        code=1,
        msg="ID 不能为空"
    )