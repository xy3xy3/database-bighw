from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from admin.utils.commonModel import ResponseModel
from admin.utils.decorators import login_required
from fastapi import Form
import os
from models.ConfigModel import ConfigModel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
router = APIRouter()

@router.get("/setting")
@login_required
async def setting(request: Request):
    try:
        config_model = ConfigModel()
        config = config_model.get_all_configs()
    except Exception as e:
        return {"code": 1, "msg": str(e), "data": None}
    view = {"request": request, "config": config, "title": "设置", "url": "setting"}
    return templates.TemplateResponse("setting.html", view)

@router.post("/setting")
@login_required
async def save(
    request: Request,
    api_key: str = Form(...)
):
    try:
        config_model = ConfigModel()
        configs = {
            "api_key": api_key  # 保存 api_key
        }
        config_model.save_configs(configs)
        return {"code": 0, "msg": "保存成功", "data": None}
    except Exception as e:
        return {"code": 1, "msg": str(e), "data": None}
