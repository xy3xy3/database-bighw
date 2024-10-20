from sqlmodel import Field
from typing import Optional
from app.models.BaseModel import BaseModel  # 导入基类

class UserModel(BaseModel, table=True):  # 继承 BaseModel
    username: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_admin: bool = Field(default=False)
