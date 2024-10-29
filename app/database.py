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

    # 先创建 Category 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "Category" (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE,
            description TEXT,
            sort INT DEFAULT 0
        );
    """)

    # 创建 User 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "User" (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255) UNIQUE,
            hashed_password VARCHAR(255),
            balance FLOAT DEFAULT 0.0
        );
    """)

    # 创建 Product 表 (依赖 Category)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "Product" (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            price FLOAT,
            stock INT DEFAULT 0,
            sort INT DEFAULT 0,
            description TEXT,
            category_id INT,
            CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES "Category" (id)
        );
    """)

    # 创建 Order 表 (依赖 User 和 Product)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "Order" (
            id SERIAL PRIMARY KEY,
            user_id INT,
            product_id INT,
            quantity INT,
            total_price FLOAT,
            status VARCHAR(50),
            CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES "User" (id),
            CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES "Product" (id)
        );
    """)

    # 创建 Payment 表 (依赖 Order)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "Payment" (
            id SERIAL PRIMARY KEY,
            order_id INT,
            amount FLOAT,
            method VARCHAR(50),
            status VARCHAR(50),
            CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES "Order" (id)
        );
    """)

    # 创建 Config 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "Config" (
            k VARCHAR(255) PRIMARY KEY,
            v TEXT
        );
    """)

    # Config设置默认admin_user,admin_pwd
    cursor.execute("""
        INSERT INTO "Config" (k, v) VALUES ('admi_user', 'admin'), ('admin_pwd', 'admin');
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
        DROP TABLE IF EXISTS "Payment";
        DROP TABLE IF EXISTS "Order";
        DROP TABLE IF EXISTS "Product";
        DROP TABLE IF EXISTS "User";
        DROP TABLE IF EXISTS "Category";
        DROP TABLE IF EXISTS "Config";
    """)

    conn.commit()
    cursor.close()
    conn.close()