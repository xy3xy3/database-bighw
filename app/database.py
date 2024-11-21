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

    # 其他表的创建语句...

    conn.commit()
    cursor.close()
    conn.close()
def reset_db():
    """重置数据库，删除所有表"""
    conn = db.get_connection()
    cursor = conn.cursor()

    # 删除所有表（按依赖关系删除）
    cursor.execute("""
        DROP TABLE IF EXISTS "history";
        DROP TABLE IF EXISTS "message";
    """)

    conn.commit()
    cursor.close()
    conn.close()