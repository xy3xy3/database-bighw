import psycopg
from models.BaseModel import BaseModel
from database import db

class ModelModel(BaseModel):
    table_name = "model"

    def __init__(self):
        super().__init__()

    async def get_model_by_id(self, id: int):
        """根据ID获取模型信息"""
        sql = f'SELECT * FROM "{self.table_name}" WHERE id = %s;'
        async with db.pool.connection() as conn:
            async with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                await cur.execute(sql, (id,))
                model = await cur.fetchone()
                return model