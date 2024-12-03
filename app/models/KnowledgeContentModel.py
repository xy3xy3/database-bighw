import psycopg
from utils import list_to_vector
from models.BaseModel import BaseModel
from typing import List, Optional
from datetime import datetime
from database import db

class KnowledgeContentModel(BaseModel):
    table_name = "knowledge_content"

    async def save_with_embedding(self, base_id: int, content: str, embedding: List[float]):
        data = {
            "base_id": base_id,
            "content": content,
            "embedding": list_to_vector(embedding),
            "created_at": datetime.now()
        }
        return await self.save(data)

    async def get_nearest_neighbors(self, embedding: List[float], top_n: int = 5, base_ids: Optional[List[int]] = None):
        embedding_str = list_to_vector(embedding)
        sql = f'SELECT id, content FROM "{self.db_schema}"."{self.table_name}"'
        if base_ids:
            base_ids_str = ', '.join(map(str, base_ids))
            sql += f' WHERE base_id IN ({base_ids_str})'
        sql += f' ORDER BY embedding <-> %s LIMIT %s'
        async with db.pool.connection() as conn:
            async with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                await cur.execute(sql, (embedding_str, top_n))
                return await cur.fetchall()

    async def get_content_by_base_id(self, base_id: int):
        return await self.query({"base_id": base_id})