from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from admin.utils.commonModel import ResponseModel
from admin.utils.decorators import login_required
from database import db
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
router = APIRouter()


@router.get("/")
@login_required
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/console")
@login_required
async def console(request: Request):
    return templates.TemplateResponse("console.html", {"request": request})