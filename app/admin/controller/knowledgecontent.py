from fastapi import APIRouter, Request, Form
from typing import Optional
from admin.utils.commonModel import ResponseModel
from admin.utils.decorators import login_required
from models.KnowledgeContentModel import KnowledgeContentModel

router = APIRouter()

# 知识库内容 - 搜索
@router.post("/knowledgecontent/search")
@login_required
async def knowledgecontent_search(
    request: Request,
    page: int = Form(1),
    limit: int = Form(10),
    base_id: int = Form(...),
    keyword: Optional[str] = Form(None),
):
    model = KnowledgeContentModel()
    conditions = {"base_id": base_id}
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
    base_id = form_data.get("base_id")
    content = form_data.get("content")
    embedding = form_data.get("embedding")

    if content_id:
        data = {"base_id": base_id, "content": content, "embedding": embedding}
        model.update(int(content_id), data)
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
