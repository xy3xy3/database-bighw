# -*- coding: utf-8 -*-
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 主数据库配置
    db_host: str = "172.18.198.221"
    db_port: str = "5432"
    db_user: str = "superuser"
    db_password: str = "OGSql@123"
    db_name: str = "postgres"
    db_schema: str = "hw"

    # dataVec数据库配置
    vec_db_host = "172.18.35.21"
    vec_db_port = "5433"
    vec_db_user = "gaussdb"
    vec_db_password = "OGSql@123"
    vec_db_name = "postgres"
    vec_db_schema = "postgres"

    class Config:
        env_file = ".env"  # 如果需要从环境变量文件中读取配置
        env_prefix = "APP_"  # 环境变量前缀

settings = Settings()