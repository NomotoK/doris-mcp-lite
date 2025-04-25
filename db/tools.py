import re
from db import DorisConnector
from server import mcp
from mcp.server.fastmcp import Context
from mcp.server.fastmcp.tools import Tool




class SQLTools:
    def __init__(self):
        self.db = DorisConnector()

    def _is_safe_select(self, sql: str) -> bool:
        """
        检查 SQL 是否为安全的 SELECT 查询
        """
        sql = sql.strip().lower()
        return sql.startswith("select") and not re.search(r"\b(update|delete|insert|drop|alter|create|replace|truncate)\b", sql)
    


    @mcp.tool(name="run_select_query")
    def run_select_query(self, sql: str) -> str:
        """
        执行只读 SELECT 查询并返回格式化结果。
        """
        if not self._is_safe_select(sql):
            return "仅允许只读 SELECT 查询，不支持修改型语句。"

        try:
            rows = self.db.execute_query(sql)
            if not rows:
                return "查询结果为空。"

            # 格式化结果为字符串表格
            headers = rows[0].keys()
            lines = [" | ".join(headers)]
            lines.append("-" * len(lines[0]))
            for row in rows:
                lines.append(" | ".join(str(row[col]) for col in headers))
            return "\n".join(lines)
        except Exception as e:
            return f"查询失败: {str(e)}"
        


    @mcp.tool(name="preview_table")
    def preview_table(self, table_name: str) -> str:
        """
        预览指定表前 10 行数据。
        """
        try:
            sql = f"SELECT * FROM {table_name} LIMIT 10;"
            return self.run_select_query(sql)
        except Exception as e:
            return f"预览失败: {str(e)}"
        

        
    @mcp.tool(name="describe_table")
    def describe_table(self, table_name: str) -> str:
        """
        返回指定表的字段结构，包括字段名、类型、是否为 null、默认值和注释。
        """
        try:
            schema = self.db.get_table_schema(table_name)
            if not schema:
                return f"表 `{table_name}` 不存在或无法获取结构信息。"

            # 提取字段并构建格式化表格
            headers = ["Field", "Type", "Null", "Key", "Default", "Extra"]
            lines = [" | ".join(headers)]
            lines.append("-" * len(lines[0]))

            for row in schema:
                line = " | ".join(str(row.get(h.lower(), "")) for h in headers)
                lines.append(line)

            return "\n".join(lines)

        except Exception as e:
            return f"获取表结构失败: {str(e)}"
        


    @mcp.tool(name="list_all_tables")
    def list_all_tables(self, db_name) -> str:
        """
        列出当前数据库的所有表。
        """
        try:
            tables = self.db.list_tables(db_name)
            return "\n".join(tables)
        except Exception as e:
            return f"无法获取表列表: {str(e)}"