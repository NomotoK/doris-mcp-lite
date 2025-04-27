from doris_mcp_server.mcp_app import mcp
from doris_mcp_server.db import DorisConnector
from doris_mcp_server.config import DB_CONFIG
from typing import Optional

def _get_table_schemas(db_name: str) -> dict[str, str]:
    """
    获取所有表的结构信息，返回一个字典：
    {
        "table_name": "字段名 | 类型 | 是否为空 ... \n ...",
        ...
    }
    """
    db = DorisConnector()
    tables = db.list_tables(db_name)
    result = {}

    for table in tables:
        try:
            schema = db.get_table_schema(table)
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




def _get_table_comments(db_name: str) -> dict[str, str]:
    """
    获取所有表的注释信息，返回一个字典：
    {
        "table_name": "表注释",
        ...
    }
    """
    db = DorisConnector()
    sql = f"""
    SELECT TABLE_NAME, TABLE_COMMENT
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = '{db_name}'
    """
    try:
        results = db.execute_query(sql)
        return {row["TABLE_NAME"]: row["TABLE_COMMENT"] or "无注释" for row in results}
    except Exception as e:
        return {"error": f"无法获取表注释信息: {str(e)}"}
    



@mcp.resource("doris://schema/{db_name}")
def all_table_schemas(db_name: str = DB_CONFIG["database"]) -> str:
    """
    返回指定数据库下所有表的结构。
    """
    schemas = _get_table_schemas(db_name)

    content = []
    for table_name, schema_text in schemas.items():
        content.append(f"# 表: {table_name}\n{schema_text}\n")

    return "\n\n".join(content)




@mcp.resource("doris://schema/{table}")
def table_schema(table: str) -> Optional[str]:
    """
    返回单个表的字段结构信息。
    """
    db = DorisConnector()
    try:
        schema = db.get_table_schema(table)
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
    



@mcp.resource("doris://table-comments/{db_name}")
def all_table_comments(db_name: str = DB_CONFIG["database"]) -> str:
    """
    返回指定数据库下所有表的注释信息。
    """
    comments = _get_table_comments(db_name)
    content = []
    for table_name, comment in comments.items():
        content.append(f"- {table_name}: {comment}")
    return "\n".join(content)