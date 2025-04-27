import pymysql
from pymysql.cursors import DictCursor
from doris_mcp_server.config import DB_CONFIG


class DorisConnector:
    def __init__(self):
        self.connection = None
        self._connect()

    def _connect(self):
        try:
            self.connection = pymysql.connect(
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                database=DB_CONFIG["database"],
                cursorclass=DictCursor,
                autocommit=True
            )
            print(f"[DorisConnector] Connected to {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        except Exception as e:
            print(f"[DorisConnector] Connection failed: {e}")
            raise

    def close(self):
        if self.connection:
            self.connection.close()
            print("[DorisConnector] Connection closed.")

    def execute_query(self, sql: str) -> list[dict]:
        if not self.connection:
            self._connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
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
        return [row[f'Tables_in_{DB_CONFIG["database"]}'] for row in result]
