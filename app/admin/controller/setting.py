from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from admin.utils.commonModel import ResponseModel
from admin.utils.decorators import login_required
from models.MessageModel import MessageModel
from models.HistoryModel import HistoryModel  # 导入 HistoryModel
from fastapi import Form
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
router = APIRouter()

@router.get("/setting")
async def setting(request: Request):
    try:
        config = {}
    except Exception as e:
        return {"code": 1, "msg": str(e), "data": None}
    view = {"request": request, "config": config, "title":"设置", "url":"setting"}
    return templates.TemplateResponse("setting.html", view)

@router.post("/setting", response_model=ResponseModel, tags=["Admin"])
async def save(
    smtp_server: str = Form(...),
    smtp_port: str = Form(...),
    smtp_user: str = Form(...),
    smtp_password: str = Form(...)
)
   pass