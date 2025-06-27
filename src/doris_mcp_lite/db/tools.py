import re
from mcp.server.fastmcp import Context
from doris_mcp_lite.db import DorisConnector
from doris_mcp_lite.mcp_app import mcp
from doris_mcp_lite.config import get_db_config




def _is_safe_select(sql: str) -> bool:
    """
    检查 SQL 是否为安全的 SELECT 查询
    """
    sql = sql.strip().lower()
    return sql.startswith("select") and not re.search(r"\b(update|delete|insert|drop|alter|create|replace|truncate)\b", sql)



@mcp.tool(name="run_select_query",description="run a read-only select query and return formatted result")
async def run_select_query(sql: str, ctx: Context) -> str:
    """
    执行只读 SELECT 查询并返回格式化结果。
    """
    if not _is_safe_select(sql):
        return "仅允许只读 SELECT 查询，不支持修改型语句。"

    try:
        async with DorisConnector() as db:
            rows = await db.execute_query(sql)
            if not rows:
                return "查询结果为空。"

            headers = rows[0].keys()
            lines = [" | ".join(headers)]
            lines.append("-" * len(lines[0]))

            total = len(rows)
            for idx, row in enumerate(rows):
                await ctx.report_progress(idx + 1, total)
                lines.append(" | ".join(str(row[col]) for col in headers))
            return "\n".join(lines)
    except Exception as e:
        return f"查询失败: {str(e)}"



@mcp.tool(name="preview_table",description="preview the first 10 rows of a table")
async def preview_table(table_name: str) -> str:
    """
    预览指定表前 10 行数据。
    """
    try:
        sql = f"SELECT * FROM {table_name} LIMIT 10;"
        return await run_select_query(sql)
    except Exception as e:
        return f"预览失败: {str(e)}"




@mcp.tool(name="describe_table",description="return the structure of a table, including field names, types, nullability, default values, and comments")
async def describe_table(table_name: str) -> str:
    """
    返回指定表的字段结构，包括字段名、类型、是否为 null、默认值和注释。
    """
    try:
        async with DorisConnector() as db:
            schema = await db.get_table_schema(table_name)
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




@mcp.tool(name="list_all_tables",description="list all tables in the current database")
async def list_all_tables(db_name: str = None) -> str:
    """
    列出当前数据库的所有表。
    """
    if db_name is None:
        db_name = get_db_config()["database"]

    try:
        async with DorisConnector() as db:
            tables = await db.list_tables(db_name)
            return "\n".join(tables)
    except Exception as e:
        return f"无法获取表列表: {str(e)}"
    
