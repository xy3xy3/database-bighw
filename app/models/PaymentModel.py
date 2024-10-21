from sqlmodel import Field, Relationship
from typing import Optional
from models.BaseModel import BaseModel
from models.OrderModel import OrderModel

class PaymentModel(BaseModel, table=True):
    order_id: Optional[int] = Field(default=None, foreign_key="ordermodel.id")
    amount: float
    payment_method: str  # 如 "credit_card", "paypal" 等
    payment_status: str  # 如 "completed", "pending", "failed" 等

    # 关系 - 每个支付信息对应一个订单
    order: Optional["OrderModel"] = Relationship(back_populates="payment")
