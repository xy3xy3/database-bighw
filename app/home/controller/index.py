from typing import Optional
from fastapi import APIRouter, Request, Depends
from home.utils.Templates import Templates
from home.utils.commonModel import ResponseModel
from home.utils.decorators import login_required
from database import db
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Templates(directory=TEMPLATES_DIR)
router = APIRouter()


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})