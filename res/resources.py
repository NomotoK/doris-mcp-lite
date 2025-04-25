from server import mcp
from mcp.server.fastmcp import resources
from db.db import DorisConnector
from typing import Optional


class DorisSchemaResource:
    def __init__(self):
        self.db = DorisConnector()

    def get_table_schemas(self,db_name) -> dict[str, str]:
        """
        获取所有表的结构信息，返回一个字典：
        {
            "table_name": "字段名 | 类型 | 是否为空 ... \n ...",
            ...
        }
        """
        tables = self.db.list_tables(db_name)
        result = {}

        for table in tables:
            try:
                schema = self.db.get_table_schema(table)
                if not schema:
                    continue

                # 提取字段结构
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

    @mcp.resource("doris://schema/{db_name}")
    def all_table_schemas(self,db_name: str) -> str:
        """
        暴露指定数据库下所有表结构为资源（纯文本格式）
        """
        schemas = self.get_table_schemas(db_name)
        content = []

        for table_name, schema_text in schemas.items():
            content.append(f"# 表: {table_name}\n{schema_text}\n")

        return "\n\n".join(content)


    @mcp.resource("doris://schema/{table}")
    def table_schema(self, table: str) -> Optional[str]:
        """
        暴露指定表的结构为独立资源：doris://schema/{table}
        """
        try:
            schema = self.db.get_table_schema(table)
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