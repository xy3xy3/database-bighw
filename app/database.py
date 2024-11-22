import psycopg2
from psycopg2 import pool
from config import settings
import logging

class Database:
    def __init__(self):
        logging.info(f"Database schema: {settings.db_schema}")
        self.connection_pool = pool.SimpleConnectionPool(
            1,  # 最小连接数
            10,  # 最大连接数
            user=settings.db_user,
            password=settings.db_password,
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_name,
            options=f"-c search_path={settings.db_schema}"
        )

    def get_connection(self):
        return self.connection_pool.getconn()

    def release_connection(self, conn):
        self.connection_pool.putconn(conn)

    def close_all(self):
        self.connection_pool.closeall()

db = Database()

# File: app\database.py
def init_db():
    """初始化数据库，创建所需的表"""
    conn = db.get_connection()
    cursor = conn.cursor()

    # 创建 history 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            agent_id INTEGER
        );
    """)

    # 创建 message 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS message (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            history_id INTEGER,
            role VARCHAR(50),
            content TEXT
        );
    """)

    # 创建 model 表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS model (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        base_url VARCHAR(255) NOT NULL,
        api_key VARCHAR(255) NOT NULL,
        type INT NOT NULL
    );  
    """)

    # 创建 knowledgebase 表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledgebase (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        model_id INT NOT NULL
    );  
    """)

    # 其他表的创建语句...
    # 创建 Config 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "config" (
            k VARCHAR(255) PRIMARY KEY,
            v TEXT
        );
    """)

    # Config设置默认admin_user,admin_pwd
    cursor.execute("""
        INSERT INTO "config" (k, v) VALUES ('admin_user', 'admin'), ('admin_pwd', 'admin');
    """)
    conn.commit()
    cursor.close()
    conn.close()
def reset_db():
    """重置数据库，删除所有表"""
    conn = db.get_connection()
    cursor = conn.cursor()

    # 删除所有表（按依赖关系删除）
    cursor.execute("""
        DROP TABLE IF EXISTS "message";
        DROP TABLE IF EXISTS "knowledgebase";
        DROP TABLE IF EXISTS "history";
        DROP TABLE IF EXISTS "model";
        DROP TABLE IF EXISTS "config";
    """)

    conn.commit()
    cursor.close()
    conn.close()