from pydantic import BaseModel
from typing import List

class ResponseModel(BaseModel):
    code: int
    msg: str
    data: dict | list | None = None
    count: int | None = None

class BatchDeleteRequest(BaseModel):
    ids: List[int]

