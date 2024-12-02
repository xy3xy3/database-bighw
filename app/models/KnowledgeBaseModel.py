from models.BaseModel import BaseModel

from database import db

class KnowledgeBaseModel(BaseModel):
    table_name = "knowledgebase"

    async def get_model_details_by_base_id(self, base_id: int) -> dict:
        sql = f'''
            SELECT m.name AS model, m.base_url, m.api_key
            FROM "{self.db_schema}".knowledgebase kb
            JOIN "{self.db_schema}".model m ON kb.model_id = m.id
            WHERE kb.id = %s
        '''
        async with db.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, (base_id,))
                result = await cur.fetchone()
                if not result:
                    return {}
                return {
                    "model": result['model'],
                    "base_url": result['base_url'],
                    "api_key": result['api_key']
                }