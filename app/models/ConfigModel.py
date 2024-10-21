from sqlmodel import SQLModel, Field

class ConfigModel(SQLModel, table=True):
    __tablename__ = "Config"
    k: str = Field(unique=True, index=True, primary_key=True)
    v: str