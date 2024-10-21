from sqlmodel import Field, Relationship
from typing import Optional
from models.BaseModel import BaseModel
from models.OrderModel import OrderModel

class PaymentModel(BaseModel, table=True):
    __tablename__ = "Payment"
    # 关联订单，可以是充值 或者 支付订单
    order_id: Optional[int] = Field(default=None, foreign_key="Order.id")
    # 金额
    amount: float
    method: str  # 如 "credit_card", "paypal" 等
    status: str  # 如 "completed", "pending", "failed" 等