from models.BaseModel import BaseModel

class ModelModel(BaseModel):
    table_name = "model"

    def __init__(self):
        super().__init__()

    def get_model_by_id(self, id: int):
        """根据ID获取模型信息"""
        sql = f'SELECT * FROM "{self.table_name}" WHERE id = %s;'
        self.cursor.execute(sql, (id,))
        model = self.cursor.fetchone()
        return model