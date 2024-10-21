from sqlmodel import Field
from typing import Optional
from models.BaseModel import BaseModel

class ConfigModel(BaseModel, table=True):
    k: str = Field(unique=True, index=True)
    v: str