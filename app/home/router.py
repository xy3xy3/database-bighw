from fastapi import APIRouter
import os
from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from models.AgentModel import AgentModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
home_router = APIRouter()

@home_router.get("/")
async def index(request: Request):
    agent_model = AgentModel()
    models = agent_model.get_all()
    print(models)  # [{'id': 1, 'name': '中山大学助手'}]
    base_url = str(request.url).rstrip('/')
    return templates.TemplateResponse("index.html", {"request": request, "base_url": base_url, "models": models})
