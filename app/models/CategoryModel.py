from models.BaseModel import BaseModel

class CategoryModel(BaseModel):
    table_name = "Category"

    def __init__(self):
        super().__init__()

    def create_category(self, name: str, description: str = None, sort: int = 0):
        data = {
            "name": name,
            "description": description,
            "sort": sort
        }
        return self.save(data)

    def get_by_name(self, name: str):
        return self.query({"name": name})
