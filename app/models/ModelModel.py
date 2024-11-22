from models.BaseModel import BaseModel

class ModelModel(BaseModel):
    table_name = "model"

    def __init__(self):
        super().__init__()

    def create_model(self, name: str, base_url: str, api_key: str, model_type: int):
        data = {
            "name": name,
            "base_url": base_url,
            "api_key": api_key,
            "type": model_type
        }
        return self.save(data)

    def get_by_id(self, id: int):
        return super().get_by_id(id)

    def get_by_name(self, name: str):
        return self.query({"name": name})

    def update_model(self, id: int, name: str = None, base_url: str = None, api_key: str = None, model_type: int = None):
        data = {}
        if name is not None:
            data["name"] = name
        if base_url is not None:
            data["base_url"] = base_url
        if api_key is not None:
            data["api_key"] = api_key
        if model_type is not None:
            data["type"] = model_type
        return self.update(id, data)

    def delete_model(self, id: int):
        return self.delete(id)

    def get_all_models(self):
        return self.query()