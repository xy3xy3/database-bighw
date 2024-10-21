from sqlmodel import Field, Relationship
from typing import Optional, List
from models.BaseModel import BaseModel
from models.CategoryModel import CategoryModel

class ProductModel(BaseModel, table=True):
    name: str = Field(index=True)
    price: float
    stock: int = Field(default=0)
    sort: int = Field(default=0)
    description: Optional[str] = None
    category_id: Optional[int] = Field(default=None, foreign_key="categorymodel.id")
    # 关系 - 每个商品属于一个类别
    category: Optional["CategoryModel"] = Relationship(back_populates="products")
