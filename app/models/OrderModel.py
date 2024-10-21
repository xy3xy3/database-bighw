from sqlmodel import Field, Relationship
from typing import List, Optional
from models.BaseModel import BaseModel

class OrderModel(BaseModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="usermodel.id")
    total_price: float
    status: str

    # 关系 - 每个订单属于一个用户
    user: Optional["UserModel"] = Relationship(back_populates="orders")
    # 关系 - 一个订单可以包含多个商品
    product: Optional["ProductModel"] = Relationship(back_populates="orders")
