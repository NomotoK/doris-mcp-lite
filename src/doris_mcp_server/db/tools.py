import re
from doris_mcp_server.db import DorisConnector
from doris_mcp_server.mcp_app import mcp
from doris_mcp_server.config import DB_CONFIG




def _is_safe_select(sql: str) -> bool:
    """
    检查 SQL 是否为安全的 SELECT 查询
    """
    sql = sql.strip().lower()
    return sql.startswith("select") and not re.search(r"\b(update|delete|insert|drop|alter|create|replace|truncate)\b", sql)



@mcp.tool(name="run_select_query")
def run_select_query(sql: str) -> str:
    """
    执行只读 SELECT 查询并返回格式化结果。
    """
    if not _is_safe_select(sql):
        return "仅允许只读 SELECT 查询，不支持修改型语句。"

    db = DorisConnector()
    try:
        rows = db.execute_query(sql)
        if not rows:
            return "查询结果为空。"

        headers = rows[0].keys()
        lines = [" | ".join(headers)]
        lines.append("-" * len(lines[0]))
        for row in rows:
            lines.append(" | ".join(str(row[col]) for col in headers))
        return "\n".join(lines)
    except Exception as e:
        return f"查询失败: {str(e)}"



@mcp.tool(name="preview_table")
def preview_table(table_name: str) -> str:
    """
    预览指定表前 10 行数据。
    """
    try:
        sql = f"SELECT * FROM {table_name} LIMIT 10;"
        return run_select_query(sql)
    except Exception as e:
        return f"预览失败: {str(e)}"




@mcp.tool(name="describe_table")
def describe_table(table_name: str) -> str:
    """
    返回指定表的字段结构，包括字段名、类型、是否为 null、默认值和注释。
    """
    db = DorisConnector()
    try:
        schema = db.get_table_schema(table_name)
        if not schema:
            return f"表 `{table_name}` 不存在或无法获取结构信息。"

        headers = ["Field", "Type", "Null", "Key", "Default", "Extra"]
        lines = [" | ".join(headers)]
        lines.append("-" * len(lines[0]))

        for row in schema:
            line = " | ".join(str(row.get(h, "")) for h in headers)
            lines.append(line)

        return "\n".join(lines)

    except Exception as e:
        return f"获取表结构失败: {str(e)}"




@mcp.tool(name="list_all_tables")
def list_all_tables(db_name: str = DB_CONFIG["database"]) -> str:
    """
    列出当前数据库的所有表。
    """
    db = DorisConnector()
    try:
        tables = db.list_tables(db_name)
        return "\n".join(tables)
    except Exception as e:
        return f"无法获取表列表: {str(e)}"