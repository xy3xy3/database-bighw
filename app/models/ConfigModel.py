import psycopg
from typing import Optional, Dict
from database import db
from config import settings
import logging
class ConfigModel:
    table_name = "config"

    def __init__(self):
        self.db_schema = settings.db_schema

    async def save(self, data: dict) -> Optional[Dict]:
        """保存数据到表中"""
        keys = ', '.join(data.keys())
        values = ', '.join([f"%({k})s" for k in data.keys()])
        sql = f'INSERT INTO "{self.db_schema}"."{self.table_name}" ({keys}) VALUES ({values}) RETURNING *'
        async with db.pool.connection() as conn:
            async with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                try:
                    await cur.execute(sql, data)
                    result = await cur.fetchone()
                    await conn.commit()
                    return dict(result) if result else None
                except Exception as e:
                    await conn.rollback()
                    logging.error(f"保存配置时出错: {e}")
                    return None

    async def update(self, id: int, data: dict) -> bool:
        """更新表中的数据"""
        set_clause = ', '.join([f'"{k}" = %({k})s' for k in data.keys()])
        sql = f'UPDATE "{self.db_schema}"."{self.table_name}" SET {set_clause} WHERE id = %(id)s'
        data['id'] = id
        async with db.pool.connection() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(sql, data)
                    await conn.commit()
                    return True
                except Exception as e:
                    await conn.rollback()
                    logging.error(f"更新配置时出错: {e}")
                    return False

    async def create_config(self, k: str, v: str) -> Optional[Dict]:
        """创建新的配置"""
        data = {
            "k": k,
            "v": v
        }
        return await self.save(data)

    async def get_config(self, k: str) -> Optional[str]:
        """根据键获取配置值"""
        sql = f'SELECT v FROM "{self.db_schema}"."{self.table_name}" WHERE k = %s'
        async with db.pool.connection() as conn:
            async with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                try:
                    await cur.execute(sql, (k,))
                    res = await cur.fetchone()
                    return res['v'] if res else None
                except Exception as e:
                    logging.error(f"获取配置时出错: {e}")
                    return None

    async def get_all_configs(self) -> Dict[str, str]:
        """获取所有配置为字典"""
        sql = f'SELECT k, v FROM "{self.db_schema}"."{self.table_name}"'
        async with db.pool.connection() as conn:
            async with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                try:
                    await cur.execute(sql)
                    results = await cur.fetchall()
                    config_dict = {row['k']: row['v'] for row in results}
                    return config_dict
                except Exception as e:
                    logging.error(f"获取所有配置时出错: {e}")
                    return {}

    async def save_configs(self, configs: Dict[str, str]) -> bool:
        """保存配置字典，存在则更新，不存在则新增"""
        async with db.pool.connection() as conn:
            async with conn.cursor() as cur:
                try:
                    for k, v in configs.items():
                        existing = await self.get_config(k)
                        if existing is not None:
                            sql = f'UPDATE "{self.db_schema}"."{self.table_name}" SET v = %s WHERE k = %s'
                            await cur.execute(sql, (v, k))
                        else:
                            sql = f'INSERT INTO "{self.db_schema}"."{self.table_name}" (k, v) VALUES (%s, %s)'
                            await cur.execute(sql, (k, v))
                    await conn.commit()
                    return True
                except Exception as e:
                    await conn.rollback()
                    logging.error(f"保存配置字典时出错: {e}")
                    return False

    async def delete_config(self, k: str) -> bool:
        """删除配置"""
        sql = f'DELETE FROM "{self.db_schema}"."{self.table_name}" WHERE k = %s'
        async with db.pool.connection() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(sql, (k,))
                    await conn.commit()
                    return True
                except Exception as e:
                    await conn.rollback()
                    logging.error(f"删除配置时出错: {e}")
                    return False

    async def update_config(self, k: str, v: str, cur: Optional[psycopg.AsyncCursor] = None) -> bool:
        """更新配置"""
        sql = f'UPDATE "{self.db_schema}"."{self.table_name}" SET v = %s WHERE k = %s'
        if cur:
            try:
                await cur.execute(sql, (v, k))
                return True
            except Exception as e:
                logging.error(f"更新配置时出错: {e}")
                return False
        else:
            async with db.pool.connection() as conn:
                async with conn.cursor() as cur_inner:
                    try:
                        await cur_inner.execute(sql, (v, k))
                        await conn.commit()
                        return True
                    except Exception as e:
                        await conn.rollback()
                        logging.error(f"更新配置时出错: {e}")
                        return False

    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """异步上下文管理器退出"""
        pass
