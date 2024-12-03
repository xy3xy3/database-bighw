import psycopg
from typing import Any, Dict, Optional
from database import db
from config import settings
from psycopg.rows import DictRow

class BaseModel:
    table_name: str  # 子类需要定义表名

    def __init__(self):
        self.db_schema = settings.db_schema

    async def save(self, data: dict):
        """保存数据到表中"""
        async with db.pool.connection() as conn:
            async with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                keys = ', '.join(data.keys())
                values = ', '.join([f"%({k})s" for k in data.keys()])
                sql = f'INSERT INTO "{self.db_schema}"."{self.table_name}" ({keys}) VALUES ({values}) RETURNING *'
                await cur.execute(sql, data)
                result = await cur.fetchone()
                return dict(result) if result else None

    async def update(self, id: int, data: dict):
        """更新表中的数据（参数化查询版）"""
        set_clause = ', '.join([f'"{k}" = %({k})s' for k in data.keys()])
        sql = f'UPDATE "{self.db_schema}"."{self.table_name}" SET {set_clause} WHERE id = %(id)s'
        data['id'] = id
        async with db.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, data)
        return True

    async def delete(self, id: int):
        """删除表中的数据"""
        sql = f'DELETE FROM "{self.db_schema}"."{self.table_name}" WHERE id = %s'
        async with db.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, (id,))
        return True

    async def batch_delete(self, ids: list):
        """批量删除表中的数据"""
        placeholders = ', '.join(['%s' for _ in ids])
        sql = f'DELETE FROM "{self.db_schema}"."{self.table_name}" WHERE id IN ({placeholders})'
        async with db.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, ids)
        return True

    async def get_by_id(self, id: int):
        """根据ID获取单条记录"""
        sql = f'SELECT * FROM "{self.db_schema}"."{self.table_name}" WHERE id = %s'
        async with db.pool.connection() as conn:
            async with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                await cur.execute(sql, (id,))
                result = await cur.fetchone()
                return dict(result) if result else None

    async def query(self, conditions: Optional[dict] = None, order_by: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None):
        """查询数据，支持多条件、排序、分页"""
        sql = f'SELECT * FROM "{self.db_schema}"."{self.table_name}"'
        params = {}
        if conditions:
            where_clause = ' AND '.join([f"{k} = %({k})s" for k in conditions.keys()])
            sql += f" WHERE {where_clause}"
            params.update(conditions)
        if order_by:
            sql += f" ORDER BY {order_by}"
        if limit:
            sql += f" LIMIT {limit}"
        if offset:
            sql += f" OFFSET {offset}"
        async with db.pool.connection() as conn:
            async with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                await cur.execute(sql, params if params else None)
                results = await cur.fetchall()
                return [dict(row) for row in results]

    async def count(self, conditions: Optional[dict] = None):
        """获取数据总数"""
        sql = f'SELECT COUNT(*) FROM "{self.db_schema}"."{self.table_name}"'
        params = {}
        if conditions:
            where_clause = ' AND '.join([f"{k} = %({k})s" for k in conditions.keys()])
            sql += f" WHERE {where_clause}"
            params.update(conditions)
        async with db.pool.connection() as conn:
            async with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                await cur.execute(sql, params if params else None)
                result = await cur.fetchone()
                print(f"Result: {result}")  # Debugging statement
                if result is not None and len(result) > 0:
                    return int(result[0])
                else:
                    return 0

    async def get_paginated(self, page: int = 1, per_page: int = 10, conditions: Optional[dict] = None):
        """获取分页数据"""
        offset = (page - 1) * per_page
        data = await self.query(conditions=conditions, limit=per_page, offset=offset)
        total = await self.count(conditions=conditions)
        return {
            "data": data,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total // per_page) + (1 if total % per_page != 0 else 0)
        }

    async def get_map(self, source: str, target: str) -> dict:
        sql = f'SELECT "{source}", "{target}" FROM "{self.db_schema}"."{self.table_name}"'
        async with db.pool.connection() as conn:
            async with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                await cur.execute(sql)
                results = await cur.fetchall()
                mapping = {row[source]: row[target] for row in results}
                return mapping

    async def get_options_list(self, value_field: str, label_field: str, conditions: Optional[dict] = None):
        """获取选项列表，格式为 [{value: ..., label: ...}, ...]"""
        sql = f'SELECT "{value_field}" AS value, "{label_field}" AS label FROM "{self.db_schema}"."{self.table_name}"'
        params = {}
        if conditions:
            where_clause = ' AND '.join([f"{k} = %({k})s" for k in conditions.keys()])
            sql += f" WHERE {where_clause}"
            params.update(conditions)
        async with db.pool.connection() as conn:
            async with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                await cur.execute(sql, params if params else None)
                results = await cur.fetchall()
                return [dict(row) for row in results]

    # 事务管理示例
    async def begin_transaction(self):
        """手动开启事务"""
        self.transaction = self.pool.transaction()
        await self.transaction.__aenter__()

    async def commit_transaction(self):
        """提交事务"""
        await self.transaction.__aexit__(None, None, None)

    async def rollback_transaction(self):
        """回滚事务"""
        await self.transaction.__aexit__(Exception("Rollback"), None, None)