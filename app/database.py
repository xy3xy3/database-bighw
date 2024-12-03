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
        self.pool = None  # 初始为 None，稍后在异步方法中初始化

    async def init_pool(self):
        """初始化连接池"""
        logging.info("初始化数据库连接池。")
        self.pool = psycopg_pool.AsyncConnectionPool(
            conninfo=f"dbname={settings.db_name} user={settings.db_user} password={settings.db_password} host={settings.db_host} port={settings.db_port} options='-c search_path={settings.db_schema}'",
            min_size=1,
            max_size=10,
        )

    async def get_connection(self):
        logging.info("从连接池获取数据库连接。")
        if not self.pool:
            await self.init_pool()
        conn = await self.pool.acquire()
        await conn.execute(f"SET search_path TO {settings.db_schema};")
        return conn

    async def release_connection(self, conn):
        logging.info("将数据库连接释放回连接池。")
        # 重置搜索路径或其他清理操作
        await conn.execute("SET search_path TO public;")
        await self.pool.release(conn)

    async def close_all(self):
        logging.info("关闭连接池中的所有数据库连接。")
        if self.pool:
            await self.pool.close()

db = Database()

async def init_db():
    """初始化数据库，创建所需的表"""
    logging.info("初始化数据库。")
    conn = await db.get_connection()
    try:
        async with conn.cursor() as cursor:
            # 创建 message 表
            logging.info("创建 message 表（如果不存在）。")
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS message (
                    id SERIAL PRIMARY KEY,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    session_id VARCHAR(64),
                    role VARCHAR(50),
                    content TEXT
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
                    name VARCHAR(255) NOT NULL,
                    description TEXT NOT NULL,
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

            # 创建 Config 表
            logging.info("创建 config 表（如果不存在）。")
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS "config" (
                    k VARCHAR(255) PRIMARY KEY,
                    v TEXT
                );
            """)

            # 创建 Agent 表
            logging.info("创建 agent 表（如果不存在）。")
            await cursor.execute("""
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
            logging.info("插入默认记录。")
            # 禁用唯一约束检查
            await cursor.execute("SET session_replication_role = 'replica';")
            # 插入模型数据
            await cursor.execute("""
                INSERT INTO model (name, base_url, api_key, model_type)
                VALUES
                    ('embedding-3', 'https://open.bigmodel.cn/api/paas/v4', '7305f8f725fd64362176a8cc68f1d909.fHTbqG2ArlpGP901', 0),
                    ('deepseek-chat', 'https://api.deepseek.com', 'sk-19810a0dceaf405cbb5caafd3842f0b6', 1),
                    ('glm-4-long', 'https://open.bigmodel.cn/api/paas/v4', '7305f8f725fd64362176a8cc68f1d909.fHTbqG2ArlpGP901', 1)
                ON CONFLICT DO NOTHING;
            """)

            # 插入知识库数据
            await cursor.execute("""
                INSERT INTO knowledgebase (name, description, model_id)
                VALUES
                    ('中山大学知识库', '1', 1)
                ON CONFLICT DO NOTHING;
            """)

            # 插入 Agent 数据，确保 base_ids = '1'
            await cursor.execute("""
                INSERT INTO agent (name, base_ids, top_n, q_model_id, q_prompt, a_model_id, a_prompt)
                VALUES
                    ('中山大学助手', '1', 100, 2, '问题关于中山大学', 3, '回答关于中山大学问题')
                ON CONFLICT DO NOTHING;
            """)

            # Config设置默认admin_user,admin_pwd
            await cursor.execute("""
                INSERT INTO "config" (k, v)
                VALUES
                    ('admin_user', 'admin'),
                    ('admin_pwd', 'admin')
                ON CONFLICT (k) DO NOTHING;
            """)
            # 恢复外键约束检查
            logging.info("启用外键约束检查。")
            await cursor.execute("SET session_replication_role = 'origin';")
        await conn.commit()
        logging.info("数据库初始化完成。")
    except Exception as e:
        await conn.rollback()
        logging.error(f"初始化数据库时出错: {e}")
    finally:
        await db.release_connection(conn)

async def reset_db():
    """重置数据库，删除所有表"""
    logging.info("重置数据库。")
    conn = await db.get_connection()
    try:
        async with conn.cursor() as cursor:
            # 禁用外键约束检查
            logging.info("禁用外键约束检查。")
            await cursor.execute("SET session_replication_role = 'replica';")

            # 按依赖关系删除表
            logging.info("删除 agent 表（如果存在）。")
            await cursor.execute("DROP TABLE IF EXISTS agent CASCADE;")
            logging.info("删除 message 表（如果存在）。")
            await cursor.execute("DROP TABLE IF EXISTS message CASCADE;")
            logging.info("删除 knowledge_content 表（如果存在）。")
            await cursor.execute("DROP TABLE IF EXISTS knowledge_content CASCADE;")
            logging.info("删除 knowledgebase 表（如果存在）。")
            await cursor.execute("DROP TABLE IF EXISTS knowledgebase CASCADE;")
            logging.info("删除 model 表（如果存在）。")
            await cursor.execute("DROP TABLE IF EXISTS model CASCADE;")
            logging.info("删除 config 表（如果存在）。")
            await cursor.execute("DROP TABLE IF EXISTS config CASCADE;")

            await conn.commit()
            logging.info("数据库重置完成。")
    except Exception as e:
        await conn.rollback()
        logging.error(f"重置数据库时出错: {e}")
    finally:
        try:
            async with conn.cursor() as cursor:
                # 恢复外键约束检查
                logging.info("启用外键约束检查。")
                await cursor.execute("SET session_replication_role = 'origin';")
                await conn.commit()
        except Exception as e:
            logging.error(f"恢复外键约束检查时出错: {e}")
            await conn.rollback()
        await db.release_connection(conn)

# 示例调用
# 如果需要初始化数据库，请取消注释以下代码并运行
# async def main():
#     await init_db()
#     # await reset_db()

# if __name__ == "__main__":
#     asyncio.run(main())
