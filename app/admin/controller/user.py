from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from database import db
from models import UserModel

templates = Jinja2Templates(directory="admin/templates")
router = APIRouter()

@router.get("/admin/user")
async def user_list(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})

@router.get("/admin/user_form")
async def user_form(request: Request):
    user_model = UserModel()
    users = user_model.query()
    return templates.TemplateResponse("user_form.html", {"request": request, "users": users})