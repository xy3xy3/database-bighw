# -*- coding: utf-8 -*-
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 主数据库配置
    db_host: str = "172.18.35.21"
    db_port: str = "5432"
    db_user: str = "gaussdb"
    db_password: str = "OGSql@123"
    db_name: str = "postgres"
    db_schema: str = "public"

    class Config:
        env_file = ".env"  # 如果需要从环境变量文件中读取配置
        env_prefix = "APP_"  # 环境变量前缀

settings = Settings()