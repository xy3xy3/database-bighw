from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from admin.controller.commonModel import ResponseModel
from database import db
from models.CategoryModel import CategoryModel
import os

# 获取项目的根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 构建模板目录的绝对路径
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
router = APIRouter()

# 分类列表页面
@router.get("/admin/category")
async def category_list(request: Request):
    return templates.TemplateResponse("category.html", {"request": request})

# 分类表单页面
@router.get("/admin/category_form")
async def category_form(request: Request):
    return templates.TemplateResponse("category_form.html", {"request": request})

# 搜索分类
@router.post("/admin/category/search")
async def category_list_ajax(request: Request, page: int = 1, limit: int = 10,
                              name: Optional[str] = None):
    category_model = CategoryModel()
    conditions = {}
    if name:
        conditions["name"] = name
    paginated_data = category_model.get_paginated(page=page, per_page=limit, conditions=conditions)

    return ResponseModel(
        code=0,
        msg="Success",
        data=paginated_data["data"],
        count=paginated_data["total"]
    )

# 保存分类
@router.post("/admin/category/save")
async def category_save(request: Request):
    form_data = await request.form()
    category_model = CategoryModel()

    category_id = form_data.get("id")
    if category_id:
        category_id = int(category_id)
    name = form_data.get("name")
    description = form_data.get("description")
    sort = form_data.get("sort", 0)

    if category_id:
        category_model.update(category_id, {
            "name": name,
            "description": description,
            "sort": sort
        })
        msg = "分类更新成功"
    else:
        category_model.create_category(name, description, sort)
        msg = "分类创建成功"

    return ResponseModel(
        code=0,
        msg=msg
    )

# 删除分类
@router.post("/admin/category/del")
async def category_del(request: Request):
    form_data = await request.form()
    category_id = form_data.get("id")
    category_model = CategoryModel()

    if category_id:
        category_model.delete(category_id)
        return ResponseModel(
            code=0,
            msg="分类删除成功"
        )
    return ResponseModel(
        code=1,
        msg="分类 ID 不能为空"
    )
