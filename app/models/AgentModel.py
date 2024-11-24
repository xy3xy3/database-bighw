from models.BaseModel import BaseModel
from app.models.ModelModel import ModelModel
from app.models.KnowledgeBaseModel import KnowledgeBaseModel

class AgentModel(BaseModel):
    table_name = "agent"

    def __init__(self):
        super().__init__()
        self.model_model = ModelModel()
        self.knowledge_base_model = KnowledgeBaseModel()

    def create_agent(self, name: str, base_ids: str, max_ref: int, min_cor: float,
                    q_model_id: int, q_prompt: str, a_model_id: int, a_prompt: str):
        """创建新的Agent"""
        data = {
            "name": name,
            "base_ids": base_ids,
            "max_ref": max_ref,
            "min_cor": min_cor,
            "q_model_id": q_model_id,
            "q_prompt": q_prompt,
            "a_model_id": a_model_id,
            "a_prompt": a_prompt,
        }
        return self.save(data)

    def update_agent(self, id: int, **kwargs):
        """更新Agent"""
        if not kwargs:
            raise ValueError("必须提供要更新的字段")
        return self.update(id, kwargs)

    def delete_agent(self, id: int):
        """删除Agent"""
        return self.delete(id)

    def get_agent_by_id(self, id: int):
        """根据ID获取Agent及其关联的模型信息"""
        agent = self.get_by_id(id)
        if not agent:
            return None

        # 获取问题优化模型信息
        q_model = self.model_model.get_model_by_id(agent['q_model_id'])
        if not q_model:
            raise ValueError("问题优化模型未找到")

        # 获取对话模型信息
        a_model = self.model_model.get_model_by_id(agent['a_model_id'])
        if not a_model:
            raise ValueError("对话模型未找到")

        agent_details = {
            "id": agent['id'],
            "name": agent['name'],
            "base_ids": agent['base_ids'],
            "max_ref": agent['max_ref'],
            "min_cor": agent['min_cor'],
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

    def search_agents(self, name: str = None, limit: int = 10, offset: int = 0):
        """搜索Agent"""
        conditions = {}
        if name:
            conditions["name__like"] = f"%{name}%"
        return self.query(conditions=conditions, limit=limit, offset=offset)
