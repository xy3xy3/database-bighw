import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict
from database import db
from config import settings

class ConfigModel:
    table_name = "config"

    def __init__(self):
        self.conn = db.get_connection()
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        self.db_schema = settings.db_schema

    def save(self, data: dict):
        """保存数据到表中"""
        keys = ', '.join(data.keys())
        values = ', '.join([f"%({k})s" for k in data.keys()])
        sql = f'INSERT INTO "{self.db_schema}"."{self.table_name}" ({keys}) VALUES ({values}) RETURNING *'
        self.cursor.execute(sql, data)
        self.conn.commit()
        return self.cursor.fetchone()

    def update(self, id: int, data: dict):
        """更新表中的数据"""
        set_clause = ', '.join([f'"{k}" = %({k})s' for k in data.keys()])
        sql = f'UPDATE "{self.db_schema}"."{self.table_name}" SET {set_clause} WHERE id = %(id)s'
        data['id'] = id
        self.cursor.execute(sql, data)
        self.conn.commit()
        return True

    def create_config(self, k: str, v: str):
        data = {
            "k": k,
            "v": v
        }
        return self.save(data)

    def get_config(self, k: str) -> Optional[str]:
        sql = f'SELECT * FROM "{self.db_schema}"."{self.table_name}" WHERE k = %s'
        self.cursor.execute(sql, (k,))
        res = self.cursor.fetchone()
        if res:
            return res['v']
        return None

    def get_all_configs(self) -> Dict[str, str]:
        """获取所有配置为字典"""
        sql = f'SELECT k, v FROM "{self.db_schema}"."{self.table_name}"'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        config_dict = {row['k']: row['v'] for row in results}
        return config_dict

    def save_configs(self, configs: Dict[str, str]):
        """保存配置字典，存在则更新，不存在则新增"""
        for k, v in configs.items():
            existing = self.get_config(k)
            if existing is not None:
                self.update_config(k, v)
            else:
                self.create_config(k, v)

    def update_config(self, k: str, v: str):
        """更新配置"""
        sql = f'UPDATE "{self.db_schema}"."{self.table_name}" SET v = %s WHERE k = %s'
        self.cursor.execute(sql, (v, k))
        self.conn.commit()

    def delete_config(self, k: str):
        """删除配置"""
        sql = f'DELETE FROM "{self.db_schema}"."{self.table_name}" WHERE k = %s'
        self.cursor.execute(sql, (k,))
        self.conn.commit()

    def __del__(self):
        """释放连接"""
        self.cursor.close()
        db.release_connection(self.conn)
