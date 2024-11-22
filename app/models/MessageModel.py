from models.BaseModel import BaseModel

class MessageModel(BaseModel):
    table_name = "message"

    def __init__(self):
        super().__init__()