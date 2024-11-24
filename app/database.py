import psycopg2
from psycopg2 import pool
from config import settings
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        logging.info("Getting a database connection from the pool.")
        return self.connection_pool.getconn()

    def release_connection(self, conn):
        logging.info("Releasing the database connection back to the pool.")
        self.connection_pool.putconn(conn)

    def close_all(self):
        logging.info("Closing all database connections in the pool.")
        self.connection_pool.closeall()

db = Database()

def init_db():
    """初始化数据库，创建所需的表"""
    logging.info("Initializing the database.")
    conn = db.get_connection()
    cursor = conn.cursor()

    # 创建 history 表
    logging.info("Creating history table if it does not exist.")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id SERIAL PRIMARY KEY,
            flag VARCHAR(255),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            agent_id INTEGER
        );
    """)

    # 创建 message 表，添加外键依赖 history 表
    logging.info("Creating message table if it does not exist.")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS message (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            history_id INTEGER REFERENCES history(id) ON DELETE CASCADE,
            role VARCHAR(50),
            content TEXT
        );
    """)

    # 创建 model 表
    logging.info("Creating model table if it does not exist.")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS model (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            base_url VARCHAR(255) NOT NULL,
            api_key VARCHAR(255) NOT NULL,
            model_type INT NOT NULL
        );
    """)

    # 创建 knowledgebase 表，添加外键依赖 model 表
    logging.info("Creating knowledgebase table if it does not exist.")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledgebase (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            model_id INT REFERENCES model(id) ON DELETE CASCADE
        );
    """)

    # 创建 knowledge_content 表，添加外键依赖 knowledgebase 表
    logging.info("Creating knowledge_content table if it does not exist.")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_content (
            id SERIAL PRIMARY KEY,
            base_id INT REFERENCES knowledgebase(id) ON DELETE CASCADE,
            content TEXT NOT NULL,
            embedding vector(2048),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 创建 Config 表
    logging.info("Creating config table if it does not exist.")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "config" (
            k VARCHAR(255) PRIMARY KEY,
            v TEXT
        );
    """)

    # 创建 Agent 表
    logging.info("Creating agent table if it does not exist.")
    cursor.execute("""
        CREATE TABLE agent (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            base_ids TEXT NOT NULL,
            top_n INTEGER NOT NULL,
            q_model_id INTEGER NOT NULL,
            q_prompt TEXT NOT NULL,
            a_model_id INTEGER NOT NULL,
            a_prompt TEXT NOT NULL
        );
    """)

    # 插入默认数据
    logging.info("Inserting default records.")
    # 禁用唯一约束检查
    cursor.execute("SET session_replication_role = 'replica';")
    # 插入模型数据
    cursor.execute("""
        INSERT INTO model (name, base_url, api_key, model_type)
        VALUES
            ('embedding-3', 'https://open.bigmodel.cn/api/paas/v4', '7305f8f725fd64362176a8cc68f1d909.fHTbqG2ArlpGP901', 0),
            ('glm-4-flash', 'https://open.bigmodel.cn/api/paas/v4', '7305f8f725fd64362176a8cc68f1d909.fHTbqG2ArlpGP901', 1),
            ('glm-4-long', 'https://open.bigmodel.cn/api/paas/v4', '7305f8f725fd64362176a8cc68f1d909.fHTbqG2ArlpGP901', 1);
        """)

    # 插入知识库数据
    cursor.execute("""
        INSERT INTO knowledgebase (name, description, model_id)
        VALUES
            ('中山大学知识库', '1', 1);
    """)

    # 插入 Agent 数据，确保 base_ids = '1'
    cursor.execute("""
        INSERT INTO agent (name, base_ids, top_n, q_model_id, q_prompt, a_model_id, a_prompt)
        VALUES
            ('中山大学助手', '1', 100, 1, '1', 2, '1');
    """)

    # Config设置默认admin_user,admin_pwd
    cursor.execute("""
        INSERT INTO "config" (k, v)
        VALUES
            ('admin_user', 'admin'),
            ('admin_pwd', 'admin');
    """)
    # 恢复外键约束检查
    logging.info("Enabling foreign key checks.")
    cursor.execute("SET session_replication_role = 'origin';")
    conn.commit()
    cursor.close()
    conn.close()
    logging.info("Database initialization completed.")

def reset_db():
    """重置数据库，删除所有表"""
    logging.info("Resetting the database.")
    conn = db.get_connection()
    cursor = conn.cursor()

    # 禁用外键约束检查
    logging.info("Disabling foreign key checks.")
    cursor.execute("SET session_replication_role = 'replica';")

    try:
        # 按依赖关系删除表
        logging.info("Dropping agent table if it exists.")
        cursor.execute("DROP TABLE IF EXISTS agent CASCADE;")
        logging.info("Dropping message table if it exists.")
        cursor.execute("DROP TABLE IF EXISTS message CASCADE;")
        logging.info("Dropping knowledge_content table if it exists.")
        cursor.execute("DROP TABLE IF EXISTS knowledge_content CASCADE;")
        logging.info("Dropping knowledgebase table if it exists.")
        cursor.execute("DROP TABLE IF EXISTS knowledgebase CASCADE;")
        logging.info("Dropping history table if it exists.")
        cursor.execute("DROP TABLE IF EXISTS history CASCADE;")
        logging.info("Dropping model table if it exists.")
        cursor.execute("DROP TABLE IF EXISTS model CASCADE;")
        logging.info("Dropping config table if it exists.")
        cursor.execute("DROP TABLE IF EXISTS config CASCADE;")

        conn.commit()
        logging.info("Database reset completed.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Error resetting database: {e}")
    finally:
        # 恢复外键约束检查
        logging.info("Enabling foreign key checks.")
        cursor.execute("SET session_replication_role = 'origin';")
        cursor.close()
        conn.close()

# 示例调用
# init_db()
# reset_db()