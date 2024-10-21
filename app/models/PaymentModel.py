from models.BaseModel import BaseModel

class PaymentModel(BaseModel):
    table_name = "Payment"

    def __init__(self):
        super().__init__()

    def create_payment(self, order_id: int, amount: float, method: str, status: str):
        data = {
            "order_id": order_id,
            "amount": amount,
            "method": method,
            "status": status
        }
        return self.save(data)

    def get_by_order_id(self, order_id: int):
        return self.query({"order_id": order_id})
