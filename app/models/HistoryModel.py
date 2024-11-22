from models.BaseModel import BaseModel

class HistoryModel(BaseModel):
    table_name = "history"

    def __init__(self):
        super().__init__()

    def create_history(self, flag: str, agent_id: int):
        """创建新的历史记录"""
        data = {
            "flag": flag,
            "agent_id": agent_id,
        }
        return self.save(data)

    def update_history(self, id: int, **kwargs):
        """更新历史记录"""
        if not kwargs:
            raise ValueError("必须提供要更新的字段")
        return self.update(id, kwargs)

    def delete_history(self, id: int):
        """删除历史记录"""
        return self.delete(id)

    def get_history_by_id(self, id: int):
        """根据ID获取历史记录"""
        return self.get_by_id(id)

    def search_histories(self, agent_id: int = None, limit: int = 10, offset: int = 0):
        """搜索历史记录"""
        conditions = {}
        if agent_id:
            conditions["agent_id"] = agent_id
        return self.query(conditions=conditions, limit=limit, offset=offset)