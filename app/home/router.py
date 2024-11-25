from fastapi import APIRouter
import os
from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
home_router = APIRouter()

@home_router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})