from models.BaseModel import BaseModel

class ProductModel(BaseModel):
    table_name = "Product"

    def __init__(self):
        super().__init__()

    def create_product(self, name: str, price: float, stock: int, category_id: int, description: str = None):
        data = {
            "name": name,
            "price": price,
            "stock": stock,
            "category_id": category_id,
            "description": description
        }
        return self.save(data)

    def get_by_category(self, category_id: int):
        return self.query({"category_id": category_id})
