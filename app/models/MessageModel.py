from models.BaseModel import BaseModel

class MessageModel(BaseModel):
    table_name = "message"

    def __init__(self):
        super().__init__()

    def create_message(self, history_id: int, role: str, content: str):
        data = {
            "history_id": history_id,
            "role": role,
            "content": content
        }
        return self.save(data)

    def get_messages_by_history(self, history_id: int):
        return self.query({"history_id": history_id}, order_by="created_at ASC")

    def get_message_by_id(self, message_id: int):
        return self.get_by_id(message_id)