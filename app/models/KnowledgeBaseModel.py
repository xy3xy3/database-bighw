from models.BaseModel import BaseModel

class KnowledgeBaseModel(BaseModel):
    table_name = "knowledgebase"

    def __init__(self):
        super().__init__()