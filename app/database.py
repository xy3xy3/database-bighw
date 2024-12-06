import sys
import asyncio
import psycopg
import psycopg_pool
from config import settings
import logging

# Windows 特殊处理
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class Database:
    def __init__(self):
        logging.info(f"Database schema: {settings.db_schema}")
        self.pool = None

    async def init_pool(self):
        """初始化连接池"""
        logging.info("初始化数据库连接池。")
        self.pool = psycopg_pool.AsyncConnectionPool(
            conninfo=f"dbname={settings.db_name} user={settings.db_user} password={settings.db_password} host={settings.db_host} port={settings.db_port} options='-c search_path={settings.db_schema}'",
            min_size=1,
            max_size=10,
        )

    async def get_connection(self):
        """从连接池获取连接"""
        logging.info("从连接池获取数据库连接。")
        if not self.pool:
            await self.init_pool()
        conn = await self.pool.getconn()
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(f"SET search_path TO {settings.db_schema};")
            return conn
        except Exception as e:
            logging.error(f"获取数据库连接时出错: {e}")
            raise

    async def release_connection(self, conn):
        """释放连接回连接池"""
        logging.info("将数据库连接释放回连接池。")
        if self.pool and conn:
            await self.pool.putconn(conn)

    async def close_all(self):
        """关闭所有连接"""
        logging.info("关闭连接池中的所有数据库连接。")
        if self.pool:
            await self.pool.close()

db = Database()

async def init_db():
    """初始化数据库，创建所需的表"""
    logging.info("初始化数据库。")
    conn = None
    try:
        conn = await db.get_connection()
        async with conn.cursor() as cursor:
            # 创建 message 表
            logging.info("创建 message 表（如果不存在）。")
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS message (
                    id SERIAL PRIMARY KEY,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    session_id VARCHAR(64),
                    role VARCHAR(50),
                    content TEXT,
                    agent_id INT REFERENCES agent(id) ON DELETE CASCADE
                );
            """)
            await cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_session_id ON message (session_id);
            """)

            # 创建 model 表
            logging.info("创建 model 表（如果不存在）。")
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS model (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    base_url VARCHAR(255) NOT NULL,
                    api_key VARCHAR(255) NOT NULL,
                    model_type INT NOT NULL
                );
            """)

            # 创建 knowledgebase 表，添加外键依赖 model 表
            logging.info("创建 knowledgebase 表（如果不存在）。")
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS knowledgebase (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    description TEXT,
                    model_id INT REFERENCES model(id) ON DELETE CASCADE
                );
            """)

            # 创建 knowledge_content 表，添加外键依赖 knowledgebase 表
            logging.info("创建 knowledge_content 表（如果不存在）。")
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_content (
                    id SERIAL PRIMARY KEY,
                    base_id INT REFERENCES knowledgebase(id) ON DELETE CASCADE,
                    content TEXT NOT NULL,
                    embedding vector(2048),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 创建 config 表
            logging.info("创建 config 表（如果不存在）。")
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS config (
                    k VARCHAR(255) PRIMARY KEY,
                    v TEXT
                );
            """)

            # 创建 agent 表
            logging.info("创建 agent 表（如果不存在）。")
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent (
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
            logging.info("插入默认记录。")
            await cursor.execute("SET session_replication_role = 'replica';")

            # 插入模型数据
            await cursor.execute("""
                INSERT INTO model (name, base_url, api_key, model_type)
                VALUES
                    ('embedding-3', 'https://open.bigmodel.cn/api/paas/v4', '7305f8f725fd64362176a8cc68f1d909.fHTbqG2ArlpGP901', 0),
                    ('deepseek-chat', 'https://api.deepseek.com', 'sk-19810a0dceaf405cbb5caafd3842f0b6', 1),
                    ('glm-4-long', 'https://open.bigmodel.cn/api/paas/v4', '7305f8f725fd64362176a8cc68f1d909.fHTbqG2ArlpGP901', 1);
            """)

            # 插入知识库数据
            await cursor.execute("""
                INSERT INTO knowledgebase (name, description, model_id)
                VALUES
                    ('中山大学知识库', '1', 1);
            """)

            # 插入 agent 数据
            await cursor.execute("""
                INSERT INTO agent (name, base_ids, top_n, q_model_id, q_prompt, a_model_id, a_prompt)
                VALUES
                    ('中山大学助手', '1', 100, 2, '问题关于中山大学', 3, '回答关于中山大学问题');
            """)

            # 插入 config 数据
            await cursor.execute("""
                INSERT INTO config (k, v)
                VALUES
                    ('admin_user', 'admin'),
                    ('admin_pwd', 'admin'),
                    ('api_key', 'sk-123');
            """)
            await cursor.execute("SET session_replication_role = 'origin';")
            await conn.commit()
            logging.info("数据库初始化完成。")
    except Exception as e:
        logging.error(f"初始化数据库时出错: {e}")
        if conn:
            await conn.rollback()
    finally:
        if conn:
            await db.release_connection(conn)

async def reset_db():
    """重置数据库，删除所有表"""
    logging.info("重置数据库。")
    conn = None
    try:
        conn = await db.get_connection()
        async with conn.cursor() as cursor:
            # 禁用外键约束检查
            logging.info("禁用外键约束检查。")
            await cursor.execute("SET session_replication_role = 'replica';")

            # 按依赖关系删除表
            logging.info("删除所有表。")
            await cursor.execute("DROP TABLE IF EXISTS agent CASCADE;")
            await cursor.execute("DROP TABLE IF EXISTS message CASCADE;")
            await cursor.execute("DROP TABLE IF EXISTS knowledge_content CASCADE;")
            await cursor.execute("DROP TABLE IF EXISTS knowledgebase CASCADE;")
            await cursor.execute("DROP TABLE IF EXISTS model CASCADE;")
            await cursor.execute("DROP TABLE IF EXISTS config CASCADE;")

            # 恢复外键约束检查
            logging.info("恢复外键约束检查。")
            await cursor.execute("SET session_replication_role = 'origin';")

            await conn.commit()
            logging.info("数据库重置完成。")
    except Exception as e:
        logging.error(f"重置数据库时出错: {e}")
        if conn:
            await conn.rollback()
    finally:
        if conn:
            await db.release_connection(conn)
