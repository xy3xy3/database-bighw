from models.BaseModel import BaseModel

class OrderModel(BaseModel):
    table_name = "Order"

    def __init__(self):
        super().__init__()

    def create_order(self, user_id: int, product_id: int, quantity: int, total_price: float, status: str):
        data = {
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity,
            "total_price": total_price,
            "status": status
        }
        return self.save(data)

    def get_by_user(self, user_id: int):
        return self.query({"user_id": user_id})
