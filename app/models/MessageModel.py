from models.BaseModel import BaseModel

class MessageModel(BaseModel):
    table_name = "message"

    def __init__(self):
        super().__init__()

    def create_message(self, history_id: int, role: str, content: str):
        """新增一条对话消息"""
        data = {
            "history_id": history_id,
            "role": role,
            "content": content
        }
        return self.save(data)

    def update_message(self, id: int, role: str = None, content: str = None):
        """更新消息"""
        update_data = {}
        if role:
            update_data["role"] = role
        if content:
            update_data["content"] = content
        if not update_data:
            raise ValueError("必须提供要更新的字段")
        return self.update(id, update_data)

    def delete_message(self, id: int):
        """根据ID删除消息"""
        return self.delete(id)

    def get_message_by_id(self, id: int):
        """根据ID获取消息"""
        return self.get_by_id(id)

    def get_messages_by_history(self, history_id: int, limit: int = 10, offset: int = 0):
        """根据历史记录ID分页获取消息"""
        conditions = {"history_id": history_id}
        return self.query(conditions=conditions, limit=limit, offset=offset)
