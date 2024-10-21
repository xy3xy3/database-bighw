# -*- coding: utf-8 -*-
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 数据库配置
    db_host: str = "172.18.198.221"
    db_port: str = "5432"
    db_user: str = "superuser"
    db_password: str = "OGSql@123"
    db_name: str = "postgres"
    db_schema: str = "hw"

    # 其他配置（如果有）
    # ...

    class Config:
        env_file = ".env"  # 如果需要从环境变量文件中读取配置
        env_prefix = "APP_"  # 环境变量前缀

settings = Settings()