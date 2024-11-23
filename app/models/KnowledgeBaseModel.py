from models.BaseModel import BaseModel

class KnowledgeBaseModel(BaseModel):
    table_name = "knowledgebase"

    def __init__(self):
        super().__init__()
    def get_model_details_by_base_id(self, base_id: int) -> dict:
        """
        根据 base_id 获取 model、api_key 和 base_url
        """
        sql = f'''
            SELECT m.name AS model, m.base_url, m.api_key
            FROM "{self.db_schema}".knowledgebase kb
            JOIN "{self.db_schema}".model m ON kb.model_id = m.id
            WHERE kb.id = %s
        '''
        self.cursor.execute(sql, (base_id,))
        result = self.cursor.fetchone()

        if not result:
            return {}

        return {
            "model": result['model'],
            "base_url": result['base_url'],
            "api_key": result['api_key']
        }