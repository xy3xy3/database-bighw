import psycopg
from models.BaseModel import BaseModel
from models.ModelModel import ModelModel
from models.KnowledgeBaseModel import KnowledgeBaseModel
from database import db
class AgentModel(BaseModel):
    table_name = "agent"

    def __init__(self):
        super().__init__()
        self.model_model = ModelModel()
        self.knowledge_base_model = KnowledgeBaseModel()

    async def delete_agent(self, id: int):
        return await self.delete(id)

    async def get_agent_by_id(self, id: int):
        agent = await self.get_by_id(id)
        if not agent:
            return None

        q_model = await self.model_model.get_model_by_id(agent['q_model_id'])
        if not q_model:
            raise ValueError("问题优化模型未找到")

        a_model = await self.model_model.get_model_by_id(agent['a_model_id'])
        if not a_model:
            raise ValueError("对话模型未找到")

        agent_details = {
            "id": agent['id'],
            "name": agent['name'],
            "base_ids": agent['base_ids'],
            "top_n": agent['top_n'],
            "q_model": {
                "id": q_model['id'],
                "name": q_model['name'],
                "base_url": q_model['base_url'],
                "api_key": q_model['api_key'],
                "type": q_model['model_type']
            },
            "q_prompt": agent['q_prompt'],
            "a_model": {
                "id": a_model['id'],
                "name": a_model['name'],
                "base_url": a_model['base_url'],
                "api_key": a_model['api_key'],
                "type": a_model['model_type']
            },
            "a_prompt": agent['a_prompt']
        }

        return agent_details

    async def get_all(self):
        sql = f'SELECT id, name FROM "{self.db_schema}"."{self.table_name}"'
        async with db.pool.connection() as conn:
            async with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                await cur.execute(sql)
                results = await cur.fetchall()
                return [{'id': row['id'], 'name': row['name']} for row in results]

    async def search_agents(self, name: str = None, limit: int = 10, offset: int = 0):
        conditions = {}
        if name:
            conditions["name__like"] = f"%{name}%"
        return await self.query(conditions=conditions, limit=limit, offset=offset)