import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Any, Dict, Optional
from database import db
from config import settings

class BaseModel:
    table_name: str  # 子类需要定义表名
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
        # 返回插入数据的ID
        return self.cursor.fetchone()

    def update(self, id: int, data: dict):
        """更新表中的数据（拼接字符串版）"""
        set_clause = ', '.join([f'"{k}" = \'{v}\'' for k, v in data.items()])
        sql = f'UPDATE "{self.db_schema}"."{self.table_name}" SET {set_clause} WHERE id = {id}'
        print("Executing SQL:", sql)  # 输出拼接后的 SQL
        self.cursor.execute(sql)
        self.conn.commit()
        return True


    def delete(self, id: int):
        """删除表中的数据"""
        sql = f'DELETE FROM "{self.db_schema}"."{self.table_name}" WHERE id = %s'
        self.cursor.execute(sql, (id,))
        self.conn.commit()
    def batch_delete(self, ids: list):
        """批量删除表中的数据"""
        placeholders = ', '.join(['%s' for _ in ids])
        sql = f'DELETE FROM "{self.db_schema}"."{self.table_name}" WHERE id IN ({placeholders})'
        self.cursor.execute(sql, ids)
        self.conn.commit()
        return True

    def get_by_id(self, id: int):
        """根据ID获取单条记录"""
        sql = f'SELECT * FROM "{self.db_schema}"."{self.table_name}" WHERE id = %s'
        self.cursor.execute(sql, (id,))
        return self.cursor.fetchone()

    def query(self, conditions: Optional[dict] = None, order_by: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None):
        """查询数据，支持多条件、排序、分页"""
        sql = f'SELECT * FROM "{self.db_schema}"."{self.table_name}"'
        if conditions:
            where_clause = ' AND '.join([f"{k} = %({k})s" for k in conditions.keys()])
            sql += f" WHERE {where_clause}"
        if order_by:
            sql += f" ORDER BY {order_by}"
        if limit:
            sql += f" LIMIT {limit}"
        if offset:
            sql += f" OFFSET {offset}"
        print("Executing SQL:", sql)  # 输出拼接后的 SQL
        self.cursor.execute(sql, conditions)
        return self.cursor.fetchall()

    def count(self, conditions: Optional[dict] = None):
        """获取数据总数"""
        sql = f'SELECT COUNT(*) FROM "{self.db_schema}"."{self.table_name}"'
        if conditions:
            where_clause = ' AND '.join([f"{k} = %({k})s" for k in conditions.keys()])
            sql += f" WHERE {where_clause}"
        self.cursor.execute(sql, conditions)
        return self.cursor.fetchone()['count']

    def get_paginated(self, page: int = 1, per_page: int = 10, conditions: Optional[dict] = None):
        """获取分页数据"""
        offset = (page - 1) * per_page
        data = self.query(conditions=conditions, limit=per_page, offset=offset)
        total = self.count(conditions=conditions)
        return {
            "data": data,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total // per_page) + (1 if total % per_page != 0 else 0)
        }
    # 获取source->target映射，用于table的template
    def get_map(self, source: str, target: str) -> Dict[Any, Any]:
        sql = f'SELECT "{source}", "{target}" FROM "{self.db_schema}"."{self.table_name}"'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        mapping = {row[source]: row[target] for row in result}
        return mapping
    def get_options_list(self, value_field: str, label_field: str, conditions: Optional[dict] = None):
        """获取选项列表，格式为 [{value: ..., label: ...}, ...]"""
        sql = f'SELECT "{value_field}" AS value, "{label_field}" AS label FROM "{self.db_schema}"."{self.table_name}"'
        if conditions:
            where_clause = ' AND '.join([f"{k} = %({k})s" for k in conditions.keys()])
            sql += f" WHERE {where_clause}"
        self.cursor.execute(sql, conditions)
        return self.cursor.fetchall()
    # 事务管理
    def begin_transaction(self):
        """手动开启事务"""
        self.conn.autocommit = False

    def commit_transaction(self):
        """提交事务"""
        self.conn.commit()
        self.conn.autocommit = True

    def rollback_transaction(self):
        """回滚事务"""
        self.conn.rollback()
        self.conn.autocommit = True

    def __del__(self):
        """释放连接"""
        self.cursor.close()
        db.release_connection(self.conn)