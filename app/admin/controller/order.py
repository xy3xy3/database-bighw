from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from admin.utils.commonModel import ResponseModel
from admin.utils.decorators import login_required
from models.OrderModel import OrderModel
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
router = APIRouter()

# 订单列表页面
@router.get("/admin/order")
@login_required
async def order(request: Request):
    return templates.TemplateResponse("order.html", {"request": request})

# 订单表单页面
@router.get("/admin/order_form")
@login_required
async def order_form(request: Request):
    return templates.TemplateResponse("order_form.html", {"request": request})

# 搜索订单
@router.post("/admin/order/search")
@login_required
async def order_search(request: Request, page: int = 1, limit: int = 10):
    order_model = OrderModel()
    paginated_data = order_model.get_paginated(page=page, per_page=limit)
    return ResponseModel(
        code=0,
        msg="Success",
        data=paginated_data["data"],
        count=paginated_data["total"]
    )

# 保存订单
@router.post("/admin/order/save")
@login_required
async def order_save(request: Request):
    form_data = await request.form()
    order_model = OrderModel()

    order_id = form_data.get("id")
    if order_id:
        order_id = int(order_id)
    user_id = form_data.get("user_id")
    product_id = form_data.get("product_id")
    quantity = form_data.get("quantity")
    total_price = form_data.get("total_price")
    status = form_data.get("status")

    if order_id:
        order_model.update(order_id, {
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity,
            "total_price": total_price,
            "status": status
        })
        msg = "订单更新成功"
    else:
        order_model.create_order(user_id, product_id, quantity, total_price, status)
        msg = "订单创建成功"

    return ResponseModel(
        code=0,
        msg=msg
    )

# 删除订单
@router.post("/admin/order/del")
@login_required
async def order_del(request: Request):
    form_data = await request.form()
    order_id = form_data.get("id")
    order_model = OrderModel()

    if order_id:
        order_model.delete(order_id)
        return ResponseModel(
            code=0,
            msg="订单删除成功"
        )
    return ResponseModel(
        code=1,
        msg="订单 ID 不能为空"
    )