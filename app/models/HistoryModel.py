from models.MessageModel import MessageModel
from models.BaseModel import BaseModel

class HistoryModel(BaseModel):
    table_name = "history"

    def __init__(self):
        super().__init__()

    def create_history(self, agent_id: int):
        data = {
            "agent_id": agent_id
        }
        return self.save(data)

    def get_history_by_agent(self, agent_id: int):
        return self.query({"agent_id": agent_id}, order_by="created_at DESC")

    def get_history_messages(self, history_id: int):
        message_model = MessageModel()
        return message_model.get_messages_by_history(history_id)