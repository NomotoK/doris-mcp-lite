import pymysql
from pymysql.cursors import DictCursor
from doris_mcp_server.config import get_db_config
from dbutils.pooled_db import PooledDB
class DorisPool:
    _pool = None

    @classmethod
    def init_pool(cls, config):
        if cls._pool is None:
            cls._pool = PooledDB(
                creator=pymysql,
                maxconnections=8,
                mincached=2,
                blocking=True,
                host=config["host"],
                port=config["port"],
                user=config["user"],
                password=config["password"],
                database=config["database"],
                cursorclass=DictCursor,
                autocommit=True
            )

    @classmethod
    def get_connection(cls):
        if cls._pool is None:
            raise RuntimeError("Connection pool is not initialized")
        return cls._pool.connection()


class DorisConnector:
    def __init__(self, config: dict = None):
        self.config = config or get_db_config()
        DorisPool.init_pool(self.config)


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # No cleanup needed for connection pool

    def execute_query(self, sql: str) -> list[dict]:
        try:
            with DorisPool.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    return cursor.fetchall()
        except Exception as e:
            print(f"[DorisConnector] Query failed: {e}")
            raise

    def get_table_schema(self, table_name: str) -> list[dict]:
        """
        获取指定表的字段信息，包括字段名、类型、是否为空、默认值等
        """
        sql = f"DESCRIBE {table_name};"
        return self.execute_query(sql)

    def list_tables(self, db: str) -> list[str]:
        """
        获取当前数据库中所有表的列表
        """
        sql = f"SHOW TABLES IN {db};"
        result = self.execute_query(sql)
        return [row[f'Tables_in_{self.config["database"]}'] for row in result]
