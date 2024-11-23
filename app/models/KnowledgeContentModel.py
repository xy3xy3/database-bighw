from utils import list_to_vector
from models.BaseModel import BaseModel
from typing import List, Optional
from datetime import datetime

class KnowledgeContentModel(BaseModel):
    table_name = "knowledge_content"

    def __init__(self):
        super().__init__()

    def save_with_embedding(self, base_id: int, content: str, embedding: List[float]):
        """
        保存数据到表中，并处理 embedding 字段。
        """
        data = {
            "base_id": base_id,
            "content": content,
            "embedding": list_to_vector(embedding),
            "created_at": datetime.now()  # 自动填写 created_at 字段
        }
        return self.save(data)

    def get_nearest_neighbors(self, embedding: List[float], top_n: int = 5, base_id: Optional[int] = None):
        """
        获取最近邻，输入 embedding，返回 top_n 个最近邻。
        如果提供了 base_id，则只返回该 base_id 下的最近邻。
        """
        embedding_str = list_to_vector(embedding)
        sql = f'SELECT id,content FROM "{self.db_schema}"."{self.table_name}"'
        if base_id:
            sql += f' WHERE base_id = %s'
            sql += f' ORDER BY embedding <-> %s LIMIT %s'
            self.cursor.execute(sql, (base_id, embedding_str, top_n))
        else:
            sql += f' ORDER BY embedding <-> %s LIMIT %s'
            self.cursor.execute(sql, (embedding_str, top_n))

        return self.cursor.fetchall()

    def get_content_by_base_id(self, base_id: int):
        """
        根据 base_id 获取 content 数据。
        """
        return self.query({"base_id": base_id})