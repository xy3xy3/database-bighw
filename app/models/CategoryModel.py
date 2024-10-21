from sqlmodel import Field, Relationship
from typing import List, Optional
from models.BaseModel import BaseModel

class CategoryModel(BaseModel, table=True):
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None
    sort: int = Field(default=0)