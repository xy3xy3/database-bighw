from sqlmodel import Field, Relationship
from typing import List, Optional
from models.BaseModel import BaseModel

class OrderModel(BaseModel, table=True):
    __tablename__ = "Order"
    # 关联下单用户
    user_id: Optional[int] = Field(default=None, foreign_key="User.id")
    # 关联产品
    product_id : Optional[int] = Field(default=None, foreign_key="Product.id")
    quantity: int
    total_price: float
    status: str
