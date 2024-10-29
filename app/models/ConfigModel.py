import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
from database import db
from config import settings

class ConfigModel():
    table_name = "Config"

    def __init__(self):
        self.conn = db.get_connection()
        self.cursor = self.conn.cursor()

    def create_config(self, k: str, v: str):
        data = {
            "k": k,
            "v": v
        }
        return self.save(data)

    def get_config(self, k: str):
        sql = f'SELECT * FROM "{settings.db_schema}"."{self.table_name}" WHERE k = %s'
        self.cursor.execute(sql, (k,))
        res = self.cursor.fetchone()# tuple
        if res:
            return res[1]
        return None
