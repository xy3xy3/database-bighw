from fastapi import APIRouter, Request, Form
from typing import Optional
from admin.utils.commonModel import ResponseModel
from admin.utils.decorators import login_required
from models.KnowledgeContentModel import KnowledgeContentModel
from models.KnowledgeBaseModel import KnowledgeBaseModel
from fastapi.templating import Jinja2Templates
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

router = APIRouter()

# 知识库列表页面
@router.get("/knowledgecontent")
@login_required
async def knowledgecontent_list(request: Request):
    return templates.TemplateResponse("knowledgecontent.html", {"request": request})

# 知识库表单页面
@router.get("/knowledgecontent_form")
@login_required
async def knowledgecontent_form(request: Request):
    knowledgebase_model = KnowledgeBaseModel()  # 实例化知识库数据访问对象
    knowledgebases = knowledgebase_model.get_options_list("id", "name")  # 获取知识库列表
    return templates.TemplateResponse("knowledgecontent_form.html", {"request": request, "knowledgebases": knowledgebases})

# 知识库内容 - 搜索
@router.post("/knowledgecontent/search")
@login_required
async def knowledgecontent_search(
    request: Request,
    page: int = Form(1),
    limit: int = Form(10),
    base_id: Optional[int] = Form(None),
    keyword: Optional[str] = Form(None),
):
    model = KnowledgeContentModel()
    conditions = {}
    if base_id:
        conditions['base_id'] = base_id
    if keyword:
        conditions["content"] = f"%{keyword}%"  # 支持模糊查询
    paginated_data = model.get_paginated(page=page, per_page=limit, conditions=conditions)
    return ResponseModel(
        code=0,
        msg="Success",
        data=paginated_data["data"],
        count=paginated_data["total"]
    )

# 知识库内容 - 保存
@router.post("/knowledgecontent/save")
@login_required
async def knowledgecontent_save(request: Request):
    form_data = await request.form()
    model = KnowledgeContentModel()

    content_id = form_data.get("id")
    if content_id:
        content_id = int(content_id)
    base_id = form_data.get("base_id")
    content = form_data.get("content")
    embedding = form_data.get("embedding")

    if content_id:
        data = {"base_id": base_id, "content": content, "embedding": embedding}
        model.update(content_id, data)
        msg = "知识库内容更新成功"
    else:
        data = {"base_id": base_id, "content": content, "embedding": embedding}
        model.save(data)
        msg = "知识库内容创建成功"

    return ResponseModel(code=0, msg=msg)

# 知识库内容 - 删除
@router.post("/knowledgecontent/del")
@login_required
async def knowledgecontent_del(request: Request):
    form_data = await request.form()
    content_id = form_data.get("id")
    model = KnowledgeContentModel()

    if content_id:
        model.delete(int(content_id))
        return ResponseModel(code=0, msg="知识库内容删除成功")
    return ResponseModel(code=1, msg="内容 ID 不能为空")
