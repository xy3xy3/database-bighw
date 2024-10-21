from sqlmodel import SQLModel, Field
from typing import Optional

class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    __table_args__ = {"extend_existing": True}
