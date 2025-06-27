from doris_mcp_lite.mcp_app import mcp
from doris_mcp_lite.db import DorisConnector
from doris_mcp_lite.config import get_db_config
from typing import Optional

async def _get_table_schemas(db_name: str) -> dict[str, str]:
    """
    获取所有表的结构信息，返回一个字典：
    {
        "table_name": "字段名 | 类型 | 是否为空 ... \n ...",
        ...
    }
    """
    async with DorisConnector() as db:
        tables = await db.list_tables(db_name)
    result = {}

    for table in tables:
        try:
            async with DorisConnector() as db:
                schema = await db.get_table_schema(table)
            if not schema:
                continue

            headers = ["Field", "Type", "Null", "Key", "Default", "Extra"]
            lines = [" | ".join(headers)]
            lines.append("-" * len(lines[0]))

            for row in schema:
                line = " | ".join(str(row.get(h, "")) for h in headers)
                lines.append(line)

            result[table] = "\n".join(lines)

        except Exception as e:
            result[table] = f"无法获取表结构: {str(e)}"

    return result




async def _get_table_comments(db_name: str) -> dict[str, str]:
    """
    获取所有表的注释信息，返回一个字典：
    {
        "table_name": "表注释",
        ...
    }
    """
    sql = f"""
    SELECT TABLE_NAME, TABLE_COMMENT
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = '{db_name}'
    """
    try:
        async with DorisConnector() as db:
            results = await db.execute_query(sql)
        return {row["TABLE_NAME"]: row["TABLE_COMMENT"] or "无注释" for row in results}
    except Exception as e:
        return {"error": f"无法获取表注释信息: {str(e)}"}
    



@mcp.resource("doris://schema/{db_name}")
async def all_table_schemas(db_name: str = None) -> str:
    """
    返回指定数据库下所有表的结构。
    """
    if db_name is None:
        db_name = get_db_config()["database"]

    schemas = await _get_table_schemas(db_name)

    content = []
    for table_name, schema_text in schemas.items():
        content.append(f"# 表: {table_name}\n{schema_text}\n")

    return "\n\n".join(content)




@mcp.resource("doris://schema/{table}")
async def table_schema(table: str) -> Optional[str]:
    """
    返回单个表的字段结构信息。
    """
    try:
        async with DorisConnector() as db:
            schema = await db.get_table_schema(table)
            if not schema:
                return f"表 `{table}` 不存在或无结构信息。"

            headers = ["Field", "Type", "Null", "Key", "Default", "Extra"]
            lines = [" | ".join(headers)]
            lines.append("-" * len(lines[0]))

            for row in schema:
                lines.append(" | ".join(str(row.get(h, "")) for h in headers))

            return f"# 表: {table}\n" + "\n".join(lines)

    except Exception as e:
        return f"无法获取表 `{table}` 的结构信息: {str(e)}"
    


@mcp.resource("doris://table-rowcount/{table}")
async def get_table_rowcount(table: str) -> str:
    """
    返回指定表的行数。
    """
    try:
        async with DorisConnector() as db:
            sql = f"SELECT COUNT(*) AS row_count FROM {table}"
            result = await db.execute_query(sql)
            if result:
                return f"表 `{table}` 的行数为: {result[0]['row_count']}"
            else:
                return f"表 `{table}` 不存在或无法获取行数。"
    except Exception as e:
        return f"获取表 `{table}` 行数失败: {str(e)}"


@mcp.resource("doris://table-comments/{db_name}")
async def all_table_comments(db_name: str = None) -> str:
    """
    返回指定数据库下所有表的注释信息。
    """
    if db_name is None:
        db_name = get_db_config()["database"]
    comments = await _get_table_comments(db_name)
    content = []
    for table_name, comment in comments.items():
        content.append(f"- {table_name}: {comment}")
    return "\n".join(content)