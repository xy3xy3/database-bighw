from sqlmodel import SQLModel, Field
from typing import Optional

class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

    # 自动生成 __tablename__，使用类名转换为小写的表名
    @classmethod
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    __table_args__ = {"extend_existing": True}
