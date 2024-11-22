from models.BaseModel import BaseModel

class HistoryModel(BaseModel):
    table_name = "history"

    def __init__(self):
        super().__init__()

    def create_history(self, flag: str, agent_id: int):
        data = {
            "flag": flag,
            "agent_id": agent_id
        }
        return self.save(data)

    def get_by_agent_id(self, agent_id: int):
        return self.query({"agent_id": agent_id})