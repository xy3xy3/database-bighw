from sqlmodel import Field
from typing import Optional
from models.BaseModel import BaseModel

class UserModel(BaseModel, table=True):
    username: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_admin: bool = Field(default=False)
