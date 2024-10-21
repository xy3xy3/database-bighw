from models.BaseModel import BaseModel

class ConfigModel(BaseModel):
    table_name = "Config"

    def __init__(self):
        super().__init__()

    def create_config(self, k: str, v: str):
        data = {
            "k": k,
            "v": v
        }
        return self.save(data)

    def get_config(self, k: str):
        return self.get_by_id(k)
