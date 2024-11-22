from models.BaseModel import BaseModel

class KnowledgeContentModel(BaseModel):
    table_name = "knowledge_content"

    def __init__(self):
        super().__init__()
