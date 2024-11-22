from models.BaseModel import BaseModel

class HistoryModel(BaseModel):
    table_name = "history"

    def __init__(self):
        super().__init__()