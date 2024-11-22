from models.BaseModel import BaseModel

class AgentModel(BaseModel):
    table_name = "agent"

    def __init__(self):
        super().__init__()

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
        """根据ID获取Agent"""
        return self.get_by_id(id)

    def search_agents(self, name: str = None, limit: int = 10, offset: int = 0):
        """搜索Agent"""
        conditions = {}
        if name:
            conditions["name__like"] = f"%{name}%"
        return self.query(conditions=conditions, limit=limit, offset=offset)